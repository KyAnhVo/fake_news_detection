package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func HandleUnexpectedError(err error) {
	if (err == nil){
		return
	}
	fmt.Printf("%v\n", err)
	os.Exit(1)
}

func PredictRealFakeHandler(w http.ResponseWriter, r *http.Request) {
	// Ensure method is POST
	
	if (r.Method != "POST") {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("{\"error\": \"predict_real_fake_news requires POST method}"))
		return
	}

	// Get bodyBytes

	bodyBytes, err := io.ReadAll(r.Body)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string { "error": "failure to read request body" }
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}

	// Get bodyMap from body, ensure json, ensure also 'title' and 'text' are
	// keys of such json before sending it over to model

	var bodyMap map[string]string
	err = json.Unmarshal(bodyBytes, &bodyMap)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("{\"error\": \"cannot parse request's body in JSON\"}"))
		return
	}

	if _, containsTitle := bodyMap["title"]; !containsTitle {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("{\"error\": \"predict_real_fake_news requires title key}"))
		return
	}
	if _, containsText := bodyMap["text"]; !containsText {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("{\"error\": \"predict_real_fake_news requires text key}"))
		return
	}
	
	// TODO: Send this to model via loopback:5000
}

func main() {
	http.HandleFunc("/api/predict_real_fake_news", PredictRealFakeHandler)
	http.ListenAndServe(":80", nil)
}
