import * as React from 'react';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      tickers: []
    };
  }

  componentDidMount() {
    fetch("http://127.0.0.1:3001/v1/tickers")
      .then(res => res.json())
      .then(
        (data) => {
          console.log(data)
          this.setState({
            isLoaded: true,
            tickers: data.result
          })
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    const { error, isLoaded, tickers } = this.state;
    console.log(this.state.tickers)
    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        tickers.map((ticker, index) => {
          return (
              <tr key={index}>
                  <td>{ticker.ticker}</td>
                  <td>{ticker.mean}</td>
              </tr>
          )
        })
      )
    }
  }
}

export default App;