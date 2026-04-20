# PN-BisimInspector
PN-BisimInspector is a Bachelor’s thesis project focused on developing a dedicated tool for place bisimilarity analysis within P/T Petri Nets.

## How to use it
To use the tool, you first need to model your Petri Nets. You can use the [Online Petri Net Simulator](https://petrinetsimulator.com). Once your nets are ready:

Export them as .json files.

Otherwise, you can directly write your net as a .json file following this schema:
```json
{
  "places":[
    {
      "id": "<string>", 
      "name": "<string>", 
      "nTokens": "<number>"
    }
  ], 
  "transitions":[
    {
      "id": "<string>", 
      "name": "<string>"
    }
  ], 
  "arcs":[
    {
      "id": "<string>", 
      "name": "<string>", 
      "start": "<string>", 
      "end": "<string>", 
      "weight": "<number>"
    }
  ], 
  "nPlaces": "<number>", 
  "nTransitions": "<number>", 
  "nArcs": "<number>"
}
```

Save the files as 'first_net.json' and 'second_net.json' because if no valid input is provided by the user, these will be the default values.

Place them inside the nets/ directory.
