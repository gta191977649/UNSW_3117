import React, { Component } from 'react';
import './App.css';
const API = 'http://localhost:5000/'
class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      weak:0,
      mid_weak:0,
      mid:0,
      mid_strong:0,
      strong:0,
    
      shimmer :{
        x:[],
        y:[],
      },
      freq: {
        x:[],
        y:[],
      },
      error:false
    }
    this.processdata = this.processdata.bind(this)
  }
  async processdata(data) {
    if(data) {
      this.setState({error:false})

      let sta = Object.keys(data["state"])[0]
      console.log(data.state)
      let value = data["state"][sta]
      switch(sta) {
        case "weak": 
          this.setState({weak:this.state.weak+value})
          break
        case "mid_weak": 
          this.setState({mid_weak:this.state.mid_weak+value})
          break
        case "mid": 
          this.setState({mid:this.state.mid+value})
          break
        case "mid_strong": 
          this.setState({mid_strong:this.state.mid_strong+value})
          break
        case "strong": 
          this.setState({strong:this.state.strong+value})
          break
      }
    }
  }
  async componentDidMount() {
    try {
      setInterval(async() =>{
        //this.setState({weak:this.state.weak+1})
        fetch(API)
        .then(response => response.json())
        .then(data => this.processdata(data))
      },1000) 
    } catch(e){
      console.log(e)
      this.setState({error:true})
    }
  }
  render() {
    const {weak,mid_weak,mid,mid_strong,strong} = this.state
    
    const content = <React.Fragment>
      <h1>WEAK:{weak}</h1>
      <h1>MID_WEAK:{mid_weak}</h1>
      <h1>MID:{mid}</h1>
      <h1>MID_STRONG:{mid_strong}</h1>
      <h1>STRONG:{strong}</h1>
    </React.Fragment>   

    const error = <React.Fragment>
      <h1>Net work error</h1>
    </React.Fragment>
    return (
      <div className="App">
        {this.state.error ? error : content}
      </div>
    );
  }
}

export default App;
