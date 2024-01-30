# Class 16 Lab: Serverless Functions

1. Use requests library to interact with **REST Countries API** found at <https://restcountries.com/#rest-countries>
2. Create a serverless function following Vercel’s get-started directions that handles two kinds of queries:
   - The serverless function should handle a `GET` http request with a given **country name** that **responds with a string** with the form of: "**The capital of `X` is `Y`**"
     - For example: `/capital-finder?country=Chile` should generate an http response of `The capital of Chile is Santiago`.
     - The serverless function should handle a `GET` http request with a given capital that responds with a string with the form of: **`Y` is the capital of `X`**
       - For example: `/capital-finder?capital=Santiago` should generate an http response of `Santiago is the capital of Chile`.
3. Extend the code to take in a **country** and a **capital** at same time, then generate response informing user if the values supplied were a correct county/capital match.
4. Handle the few countries with multiple capitals.
5. Add currency, national languages, etc.
6. dfs
