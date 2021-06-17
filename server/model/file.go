package model

import (
	"errors"
	"time"
)

type File struct {
	ID        uint       `gorm:"primary_key" json:"id"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt time.Time  `json:"updated_at"`
	DeletedAt *time.Time `json:"deleted_at"`
	Filename  string     `json:"filename"`
	Size      int64      `json:"size"`
	Checksum  string     `json:"checksum"`
}

// NewFile 返回一个空的File对象
func NewFile() File {
	return File{}
}

// CreateFile 在数据库中创建一个新的User记录
func CreateFile(f *File) (err error) {
	db = db.Create(f)
	if db.Error != nil {
		return db.Error
	}
	if db.RowsAffected != 1 {
		return errors.New("affected rows != 1")
	}
	return nil
}

// GetAllFiles 获取所有文件信息
func GetAllFiles() (files []File) {
	db.Model(&File{}).Find(&files)
	return
}

// GetFileByID 获取指定id的文件信息
func GetFileByID(id uint) (file File) {
	db.First(&file, id)
	return
}

// DeleteFile 删除指定id的文件信息
func DeleteFile(id uint) {
	db.Delete(&File{}, id)
}

// IsExisted 是否存在有摘要值
func IsExisted(checksum string) bool {
	var file File

	db.Model(&File{}).Where(&File{Checksum: checksum}).First(&file)

	return file.ID > 0
}