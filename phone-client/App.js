import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import SearchBar from "react-native-dynamic-search-bar";

async function queryAPI(query) {
  query = query.replace(' ', '+');
  query = 'http://127.0.0.1:5000/api?' + query;
  console.log(query);
  const resJSON = fetch(query, 
    {
      method: 'GET',
    }).then((response) => {console.log(response)});
}

export default function App() {

  const [searchText, setSearchText] = useState("");

  return (
    <View style={styles.viewStyle}>
      <Text style = {styles.header}>Newsflash</Text>
      <SearchBar
        placeholder = "Search here"
        onChangeText = {(text) => setSearchText(text)}
        onSubmitEditing = { () => {queryAPI(searchText)} }
      />
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  viewStyle: {
    justifyContent: 'center',
    alignItems: 'center',
    flex: 1,
    backgroundColor: 'black',
  },
  header: {
    fontSize: 50,
    marginBottom: 15,
    color: 'white',
  }
});
