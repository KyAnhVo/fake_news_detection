function is_fake_news() {
    // Disable all interactables (right now: a tags and button tags)
    const buttons = document.getElementsByTagName("button");
    for (const button of buttons) {
        button.disabled = true;
    }
    
    const noti = document.getElementById('running_notification')

    // set running_noti to "Analyzing program"
    noti.textContent = "Loading...";

    // get title and text from screen
    const title = document.getElementById('title').value;
    const text = document.getElementById('text').value;
    console.log(title)
    console.log(text)

    // send post request to http://localhost/api/predict_real_fake_news
    fetch('http://localhost/api/predict_real_fake_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'title': title,
            'text': text,
        }),
    })
    .then(response => response.json())
    .then(data => {
        noti.textContent = JSON.stringify(data)
    })

    // activate all buttons again
    for (const button of buttons) {
        button.disabled = false;
    }
}
