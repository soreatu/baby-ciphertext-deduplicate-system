package middleware

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
)

// AuthRequired 需要token
func AuthRequired() gin.HandlerFunc {
	return func(c *gin.Context) {
		token, err := c.Cookie("token")
		if err != nil {
			c.JSON(http.StatusAccepted, gin.H{"msg": "No cookie!"})
			c.Abort()
			return
		}

		if token != os.Getenv("TOKEN") {
			c.JSON(http.StatusAccepted, gin.H{"msg": "Unauthorized access!"})
			c.Abort()
			return
		}

		c.Next()
	}
}
