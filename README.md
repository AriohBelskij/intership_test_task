# Endpoint for rephrases ur syntax tree!

## Description
This endpoint rephrases your current sentence by switching the NP (noun phrase) with each other without losing meaning,
ofc if u place a correct tree and this tree have some rephrases versions c:

## Installation
Write in terminal
```
git clone https://github.com/AriohBelskij/intership_test_task.git
```
Open ur project and write in terminal

``` 
python -m venv venv
venv\Scripts\activate
pip install -m requirements.txt
```

## How to use
### How to run without docker - step #1
1. Open project
2. Run in terminal `uvicorn main:app --reload`
3. Go to step #2 c:

### How to run with docker - step #1
1. Run in terminal `docker build -t [your_image_name] .`
2. Run in terminal `docker run -p 8000:8000 [your_image_name] uvicorn main:app --host "0.0.0.0" --port 8000 --reload`
3. Go to step #2 :)

### After starting the app - step #2
1. Open in browser `localhost:8000/docs`
2. Open "/paraphrase" endpoint
3. Place your syntax tree in the "tree" variable
4. Place how many trees u want to get in the "limit" variable

For example, you can use this syntax tree:

```
(S(NP(NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter))(, ,)(CC or)(NP (NNP Barri) (NNP Gòtic)))(, ,)(VP(VBZ has)(NP(NP (JJ narrow) (JJ medieval) (NNS streets))(VP(VBN filled)(PP(IN with)(NP(NP (JJ trendy) (NNS bars))(, ,)(NP (NNS clubs))(CC and)(NP (JJ Catalan) (NNS restaurants))))))))
```

### 
![Example of response](https://i.ibb.co/cg6yHHj/2023-04-30-04-14-27.png)

