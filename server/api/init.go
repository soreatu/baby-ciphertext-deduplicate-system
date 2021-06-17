package api

import (
	"armory/middleware"

	"net/http"

	"github.com/gin-gonic/gin"
)

func NewRouter() *gin.Engine {
	r := gin.Default()

	// 跨域
	r.Use(middleware.Cors())
	// 访问控制
	r.Use(middleware.AuthRequired())

	// 路由
	v1 := r.Group("/api/v1")
	{
		v1.GET("/ping", Ping)

		// 上传文件
		v1.POST("/upload", Upload)
		// 下载文件
		v1.GET("/download/:id", Download)

		// 获取所有文件
		v1.GET("/files", GetFiles)
		// 删除文件
		v1.DELETE("/file/:id", DeleteFile)
	}

	return r
}

func Ping(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"msg": "pong"})
}
