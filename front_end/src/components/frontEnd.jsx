import React, { Component } from "react"
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import "./tweet_list.css"
import "./top.css"
import "./button.css"
import "./header.css"
import "./input.css"

class FrontEnd extends Component {
  constructor(props) {
    super(props)
    this.state = {
      tweets: [],
      hashtags: {},
      searchText: ""
    }
  }

  getResults = e => {
    const { searchText } = this.state
    fetch("http://localhost:5000/search", {
      method: "POST",
      body: JSON.stringify({ 'search_parameter': searchText })
    })
      .then(results => results.json())
      .then(results => {
        console.log(results.texts)
        console.log(results.hashtags)
        let tweets = Array.isArray(results.texts)
          ? results.texts
          : JSON.parse(results.texts);
        let hashtags = results.hashtags;
        this.setState({
          tweets
        })
        this.setState({
          hashtags
        })
      })
      .catch(error => console.error('Error:', error));

  }

  handleChange = e => {
    const { name, value } = e.target
    this.setState({
      [name]: value
    })
  }

  isEmpty(obj) {
    for (var key in obj) {
      if (obj.hasOwnProperty(key))
        return false;
    }
    return true;
  }
  render() {

    if (this.state.tweets.length) {
      var renderTweets = this.state.tweets.map((resultDetail, index) => {
        return <li>{resultDetail}</li>
      })
    }

    if (!this.isEmpty(this.state.hashtags)) {
      var renderHashtags = Object.keys(this.state.hashtags).map((key, index) => {
        return (<div style={{ "backgroundColor": "#000000" }} >
          <Col>
            <h1 style={{ "color": "#F38F8E" }}>{this.state.hashtags[key]}</h1>
            <p style={{ "color": "#FFFFFF" }}> {key}</p>
          </Col>

        </div >
        )
      })

    }

    return (
      <div className="style" >
        <div className="header">
          <h1>Twitter Popular Tweets Search Engine</h1>
        </div>

        <Container>
          <Row style={{ "marginTop": 10 }}>
            <Col>
              <input className="input" type="text" name="searchText" onChange={this.handleChange} />
              <button className="button" onClick={this.getResults}><i className="fab fa-twitter"></i></button>
            </Col>
          </Row>
          <Row style={{ "marginTop": 10 }}>
            <div className="tweet_list">
              <ul>{renderTweets}</ul>
            </div>
          </Row>
          <Row style={{ "marginTop": 10 }}>

            {renderHashtags}
            <h1> </h1>

          </Row>

        </Container>
      </div>
    )
  }
}

export default FrontEnd
