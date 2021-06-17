package api

import (
	"armory/model"
	"armory/util"
	"fmt"
	"io"
	"net/http"
	"os"
	"path"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
)

// Upload 处理上传文件请求
func Upload(c *gin.Context) {
	checksum := c.PostForm("checksum")
	if checksum == "" {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "no checksum!"})
		return
	}
	// 去重
	if model.IsExisted(checksum) {
		c.JSON(http.StatusOK, gin.H{"msg": "file exists!"})
		return
	}

	// 读取上传文件的内容
	file, err := c.FormFile("file")
	if err != nil {
		util.Log().Warning("upload file error", err)
		c.JSON(http.StatusBadRequest, gin.H{"msg": "upload file error!"})
		return
	}

	content := make([]byte, file.Size)
	src, err := file.Open()
	if err != nil {
		util.Log().Warning("open uploaded file error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "open uploaded file error!"})
		return
	}
	n, err := io.ReadFull(src, content)
	if int64(n) != file.Size || err != nil {
		util.Log().Warning("read uploaded file error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "read uploaded file error!"})
		return
	}
	_ = src.Close()

	// 校验checksum
	if util.SHA1(content) != checksum {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "unmatched checksum!"})
		return
	}
	util.Log().Info(fmt.Sprintf("Uploaded file: size %d, md5sum %s", len(content), util.SHA1(content)))

	// 将文件加密结果保存到磁盘文件中
	name := strings.Split(path.Base(file.Filename), ".")[0]
	filename := name + path.Ext(file.Filename)
	if err = saveFile(content, filename); err != nil {
		util.Log().Warning("save file error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "save file error!"})
		return
	}

	// 创建文件信息记录
	record := model.NewFile()
	record.Filename = filename
	record.Size = file.Size
	record.Checksum = checksum
	if err = model.CreateFile(&record); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "create file record error!"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"msg": fmt.Sprintf("uploaded file has been saved as %s", filename)})
}

// Download 处理文件下载
func Download(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "Invalid file id!"})
		return
	}

	// 获取文件信息
	file := model.GetFileByID(uint(id))
	if file.ID == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "File not exists!"})
		return
	}

	// 从磁盘中读取加密文件
	content, err := readFile(file.Filename, file.Size)
	if err != nil {
		util.Log().Warning("read file error", err)
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "read file error!"})
		return
	}
	util.Log().Info(fmt.Sprintf("Downloading file: name %s, size %d, md5sum %s", file.Filename, file.Size, file.Checksum))

	// 返回解密结果
	c.Writer.WriteHeader(http.StatusOK)
	c.Header("Content-Disposition", "attachment; filename="+file.Filename)
	c.Header("Content-Type", "application/octet-stream; charset=UTF-8")
	c.Header("Accept-Length", fmt.Sprintf("%d", file.Size))
	c.Writer.Write(content)
}

// GetFiles 获取当前用户的所有文件
func GetFiles(c *gin.Context) {
	files := model.GetAllFiles()
	c.JSON(http.StatusOK, gin.H{"data": files})
}

// DeleteFile 删除指定id的文件
func DeleteFile(c *gin.Context) {
	id, err := strconv.ParseUint(c.Param("id"), 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "Invalid file id!"})
		return
	}

	// 获取文件信息
	file := model.GetFileByID(uint(id))
	if file.ID == 0 {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "File not exists!"})
		return
	}

	// 删除磁盘中的文件
	if err = os.Remove(os.Getenv("UPLOAD_DIR") + "/" + file.Filename); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "Delete file error!"})
		return
	}
	// 删除文件信息记录
	model.DeleteFile(uint(id))

	c.JSON(http.StatusOK, gin.H{"msg": "Delete success!"})
}

// readFile 从磁盘中读取指定文件
func readFile(filename string, size int64) ([]byte, error) {
	content := make([]byte, size)

	src, err := os.Open(os.Getenv("UPLOAD_DIR") + "/" + filename)
	if err != nil {
		return nil, err
	}
	defer src.Close()

	_, err = src.Read(content)
	if err != nil {
		return nil, err
	}
	return content, nil
}

// saveFile 将指定文件写入磁盘中
func saveFile(content []byte, filename string) error {
	dst, err := os.Create(os.Getenv("UPLOAD_DIR") + "/" + filename)
	if err != nil {
		return err
	}
	_, err = dst.Write(content)
	return err
}
