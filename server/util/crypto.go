package util

import (
	"crypto/sha1"
	"encoding/hex"
)

func SHA1(data []byte) string {
	digest := sha1.Sum(data)
	return hex.EncodeToString(digest[:])
}
