package main

import (
	"armory/api"
	"armory/conf"
	"armory/model"
)

func main() {
	// 读取配置文件
	conf.Init()
	// 连接数据库
	model.Init()

	// 装载后端路由
	r := api.NewRouter()
	r.Run(":8081")
}
