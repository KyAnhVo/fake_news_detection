package main;

import (
	"fmt"
	"net/http"
)

func PredictRealFakeHandler(write http.ResponseWriter, read *http.Request) {
	// TODO: handle json, tcp to fake_news_identifier.py,
	// get response, and send back to user.
}

func main() {
	http.HandleFunc("/predict_real_fake", PredictRealFakeHandler)
	fmt.Println("Server listening on port 5000")
	http.ListenAndServe(":5000", nil)
}
