import requests
import re

def test_predict_real_fake():
    url = "http://localhost/api/predict_real_fake_news"

    payload = {
        "title": re.sub(
            r"\s+", " ",
            '''   2 dead at a Lexington, Kentucky, church after suspect shot a state trooper, police say. Suspect is dead   '''),

        "text": re.sub(
            r"\s+", " ",
            ''' Two women were killed in a shooting Sunday at the Richmond Road Baptist Church in Lexington, Kentucky, after a man shot a state trooper near the city’s airport, officials said. Two men were also injured in the church shooting.

The shooting near the Blue Grass Airport unfolded around 11:35 a.m. ET, after the trooper pulled over a vehicle on Terminal Drive after receiving a license plate reader alert.

The suspect fled the scene and carjacked a vehicle before ending up at Richmond Road Baptist Church about 15 miles away, Lexington Police Chief Lawrence Weathers said during a news conference Sunday.

Preliminary information suggests the suspect may have had a connection to people at the church, Weathers said without elaborating. The suspect then “fired his weapon at individuals on church property,” he said.

Three responding officers shot the suspect, who was declared dead at the scene.

The shooter has been identified, but police did not release his name. The family of the shooter has not been notified, officials said.

The victims who were killed were identified as Christina Combs, 34, and Beverly Gumm, 72. The Fayette County Coroner had earlier identified Combs as being 32.

The men who were injured in the shooting were transported to the hospital, Weathers said. One man is in critical condition, and the other is stable, he added. The injured trooper is also in stable condition.

The first shooting wasn’t connected to the airport, police said, though officials there said it impacted a portion of Terminal Drive. “Our team is on site guiding passengers to open parking. All flights and operations are now continuing as usual,” airport officials said on X. ''')
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print("Response:", response.text)
    except Exception as e:
        print("Failed to send request:", e)

if __name__ == "__main__":
    test_predict_real_fake()
