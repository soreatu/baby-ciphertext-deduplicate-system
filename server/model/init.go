package model

import (
	"os"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/sqlite"
)

var (
	// db 表示数据库对象
	db *gorm.DB
)

// Init 初始化数据库和session
func Init() {
	// 连接到数据库
	dbName := os.Getenv("DB_NAME")
	if dbName == "sqlite3" {
		sqlite3Conn(os.Getenv("DB_PATH"))
	}

	// 更新schema
	db.AutoMigrate(&File{})

	// 创建upload目录
	dirs := []string{os.Getenv("UPLOAD_DIR")}
	for _, dir := range dirs {
		if _, err := os.Stat(dir); os.IsNotExist(err) {
			err = os.MkdirAll(dir, 0755)
			if err != nil {
				panic(err)
			}
		}
	}
}

// sqlite3Conn 连接到sqlite3数据库
func sqlite3Conn(path string) {
	var err error
	db, err = gorm.Open("sqlite3", path)
	if err != nil {
		panic(err)
	}
}

