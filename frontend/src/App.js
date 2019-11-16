import React, { Component } from 'react'
import ReactEcharts from 'echarts-for-react'
import './App.css'
const API = 'http://localhost:5000/'
class App extends Component {
  constructor(props) {
    super(props)
    this.state = {
      weak: 0,
      mid_weak: 0,
      mid: 0,
      mid_strong: 0,
      strong: 0,
      shimmer: {
        x: [],
        y: [],
      },
      freq: {
        x: [],
        y: [],
      },
      error: false,
      error_msg: null,
    }
    this.processdata = this.processdata.bind(this)
  }
  getFreqOptions(){
    let freq_option = {
      textStyle:{
        color: 'rgba(255,107,107,1)',
        textShadowColor: 'rgb(255,107,107)',
        textShadowBlur: 2
      },
      xAxis: {
        type: 'category',
            data: this.state.freq.x
      },
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            color: 'rgba(255,107,107,0.3)',
            shadowColor: 'rgb(255,107,107)',
            shadowBlur: 5
          }
        }
      },
      series: [{
        data: this.state.freq.y,
        type: 'line',
        smooth: true,
        color: '#ff6b6b',
        shadowColor: 'rgb(255,41,115)',
        shadowBlur: 10,
      }]
    }
    return freq_option
  }
  getShimmerOptions(){
    let freq_option = {
      textStyle:{
        color: 'rgba(0,255,178,1)',
        textShadowColor: 'rgba(0,255,178,1)',
        textShadowBlur: 2
      },
      xAxis: {
        type: 'category',
        data: this.state.shimmer.x,

      },
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            color: 'rgba(0,255,178,0.3)',
            shadowColor: 'rgba(0,255,178,1)',
            shadowBlur: 5
          }
        }
      },
      series: [{
        data: this.state.shimmer.y,
        type: 'line',
        color: 'rgba(0,255,178,1)',
        shadowColor: 'rgb(0,255,178)',
        shadowBlur: 10,
        smooth: true,
      }]
    }
    return freq_option
  }
  async processdata(data) {
    if(data) {
      this.setState({error:false})
      let sta = Object.keys(data["state"])[0]

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
      //freq data
      let freq = {
        x: data["freq"]["x"],
        y: data["freq"]["y"],
      }
      this.setState({freq:freq})
      //shimmer data
      let shimmer = {
        x: data["shimmer"]["x"],
        y: data["shimmer"]["y"],
      }
      this.setState({shimmer:shimmer})

    }
  }
  async componentDidMount() {
    try {
      setInterval(async() =>{
        //this.setState({weak:this.state.weak+1})
        fetch(API)
        .then(response => response.json())
        .then(data => this.processdata(data))
            .catch(e => {
              this.setState({error:true,error_msg:e.toString()})
            })
      },1000) 
    } catch(e){
      console.log(e)
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

      <ReactEcharts option={this.getFreqOptions()} />
      <ReactEcharts option={this.getShimmerOptions()} />

    </React.Fragment>   

    const error = <React.Fragment>
      <h1>Net work error</h1>
      <p>{this.state.error_msg}</p>
    </React.Fragment>
    return (
      <div className="App">
        {this.state.error ? error : content}
      </div>
    );
  }
}

export default App;
