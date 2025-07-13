package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
)

// Connections to reach models

const FakeNewsPredictionContact string = "localhost:5000"

// HandleCriticalError handles critical errors that require the program
// to be stopped ASAP. Use sparingly.
func HandleCriticalError(err error) {
	if err == nil {
		return
	}
	fmt.Printf("%v\n", err)
	os.Exit(1)
}

// PredictRealFakeHandler gets a POST request and
// sends the function to localhost ip, port that links to fake_news model.
func PredictRealFakeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("----Accepted----")

	// Ensure method is POST

	if r.Method != "POST" {
		w.WriteHeader(http.StatusBadRequest)
		w.Write([]byte("{\"error\": \"predict_real_fake_news requires POST method}"))
		return
	}

	// Get bodyBytes

	bodyBytes, err := io.ReadAll(r.Body)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string{"error": "failure to read request body"}
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
		msg := map[string]string{"error": "predict_real_fake_news requires title key"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}

	if _, containsText := bodyMap["text"]; !containsText {
		w.WriteHeader(http.StatusBadRequest)
		msg := map[string]string{"error": "predict_real_fake_news requires text key"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}

	// Send this to model via corresponding contact

	msgToModelMap := map[string]string {
		"func"	: "predict_real_fake",
		"title"	:	bodyMap["title"],
		"text"	:	bodyMap["text"],
	}
	msg, _ := json.Marshal(msgToModelMap)
	fmt.Println(string(msg))
	modelConn, err := net.Dial("tcp", FakeNewsPredictionContact)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string{"error": "failure contact prediction model"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}
	fmt.Fprintf(modelConn, "%s\n", msg)

	// Receive model answer, read result, send result back to user.

	recvMsg, _ := bufio.NewReader(modelConn).ReadString('\n')
	fmt.Printf("%v\n", recvMsg)

	var recvMsgMap map[string]string
	err = json.Unmarshal([]byte(recvMsg), &recvMsgMap)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string{"error": "server message parsing / sending error"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}

	if recvMsgMap["status"] != "ok" {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string{"error": "server comm error"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}

	sendbackMsg, err := json.Marshal(map[string]string{
		"news": recvMsgMap["result"],
	})
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		msg := map[string]string{"error": "server comm error"}
		msgBytes, _ := json.Marshal(msg)
		w.Write(msgBytes)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write(sendbackMsg)
}

func main() {
	http.HandleFunc("/api/predict_real_fake_news", PredictRealFakeHandler)
	fmt.Println("----Listening----")
	http.ListenAndServe(":80", nil)
}
