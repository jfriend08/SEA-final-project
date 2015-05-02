#Data Model

```

# recommand system

Movie_Indexer = {
  key: movie-id
  value:[
      [
        'reviewer1',
        'rating1',
        'quote1'
      ],...
    ]
}

Review_Indexer = {
  key: 'critic'
  value:
  [
    [
      'movid-id',
      'rating'
    ], ...
  ]
}

Genre_Indexer = {
  key: movie
  value: [
    genre1,
    genre2,...
  ]
}

# classification system

Genres = ['Sports & Fitness', 'Comedy', 'Science Fiction & Fantasy', ...]

Weights = {
  'untamed' : [0.7464, 0.2837, 0.123, ...] , 
  'dangerously' : [0.2121, 0.3321, 0.7584, ...] ,
  ...
}

# search system

InvertedIndexer = {
  key: term
  value: {docid: tf}
    ex: {771018619: 2, 771408639: 2}

}

IdfIndexer = {
  key: term
  value: idf
}

DocumentStore = {
  key: movie-id
  value: everything from Genre_dict
}

```
