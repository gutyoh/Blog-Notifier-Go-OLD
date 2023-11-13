package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
)

const (
	ServerAddress = "127.0.0.1"
	ServerPort    = "9090"
)

func main() {
	url := fmt.Sprintf("http://%s:%s", ServerAddress, ServerPort)
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Error fetching data: %v\n", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading data: %v\n", err)
	}

	fmt.Println(string(body))
}
