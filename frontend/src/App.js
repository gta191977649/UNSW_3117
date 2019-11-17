import React, { Component } from 'react'
import ReactEcharts from 'echarts-for-react'
import './App.css'
const API = "http://"+window.location.hostname+":5000";
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
      vol:{
        x:[],
        y:[],
      },
      error: false,
      error_msg: null,
      alert:false,
    }
    this.beep = new Audio("http://nurupo27.mydns.jp/audio/beep.wav")
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
  getVolOptions(){
    let freq_option = {
      textStyle:{
        color: 'rgb(255,213,0)',
        textShadowColor: 'rgb(255,251,0)',
        textShadowBlur: 2
      },
      xAxis: {
        type: 'category',
        data: this.state.vol.x,

      },
      yAxis: {
        type: 'value',
        splitLine: {
          lineStyle: {
            color: 'rgba(255,236,0,0.3)',
            shadowColor: 'rgb(255,235,59)',
            shadowBlur: 5
          }
        }
      },
      series: [{
        data: this.state.vol.y,
        type: 'line',
        color: 'rgb(255,213,0)',
        textShadowColor: 'rgb(255,251,0)',
        shadowBlur: 10,
        smooth: true,
      }]
    }
    return freq_option
  }
  async processdata(data) {
    if(data) {
      this.setState({error:false})

      this.setState({weak:data["state"][0]})
      this.setState({mid_weak:data["state"][1]})
      this.setState({mid:data["state"][2]})
      this.setState({mid_strong:data["state"][3]})
      this.setState({strong:data["state"][4]})


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
      //vol data
      let vol = {
        x: data["vol"]["x"],
        y: data["vol"]["y"],
      }
      this.setState({vol:vol})
      //Alert
      if(data["apnea"] === true) this.beep.play()
      this.setState({alert:data["apnea"]})
    }
  }
  async fetchData() {
    fetch(API)
      .then(response => response.json())
      .then(data => this.processdata(data))
      .catch(e => {
        this.setState({error:true,error_msg:e.toString()})
        this.setState({alert:false})
      })
  }
  async componentDidMount() {
    this.fetchData()
    try {
      setInterval(async() =>{
        this.fetchData()
      },1000)
    } catch(e){
      console.log(e)
    }
  }
  render() {
    const {weak,mid_weak,mid,mid_strong,strong} = this.state
    
    const content = <React.Fragment>
      <div className="row">
        <div className="col state" style={{color:"#6cff70"}}>
          <div className="title">WEAK</div>
          <div className="value">{weak}</div>
        </div>
        <div className="col state" style={{color:"#CDDC39"}}>
          <div className="title">MID WEAK</div>
          <div className="value">{mid_weak}</div>
        </div>
        <div className="col state" style={{color:"#FFEB3B"}}>
          <div className="title">MID</div>
          <div className="value">{mid}</div>
        </div>
        <div className="col state" style={{color:"#FFC107"}}>
          <div className="title">MID STRONG</div><div className="value">{mid_strong}</div>
        </div>
        <div className="col state" style={{color:"#ff6b6b"}}>
          <div className="title">STRONG</div><div className="value">{strong}</div>
        </div>
      </div>
      <div className="text-center" style={{color:"#ff6b6b"}}><h1>FREQUENCY</h1></div>
      <ReactEcharts option={this.getFreqOptions()} />
      <div className="text-center" style={{color:"#00FFB2"}}><h1>SHIMMER</h1></div>
      <ReactEcharts option={this.getShimmerOptions()} />
      <div className="text-center" style={{color:"#FFEB3B"}}><h1>VOL</h1></div>
      <ReactEcharts option={this.getVolOptions()} />
    </React.Fragment>
    const error = <div className="text-center" style={{color:"#ff6b6b"}}>
      <h1>COMMNICATION ERROR</h1>
      <p>{this.state.error_msg}</p>
    </div>

    const alert = <div className="fixed-top text-center alert"  style={{color:"white"}}>
      <h1>ALERT</h1>
      <h3>Apnea Detected!!!</h3>
    </div>

    return (
      <div className="container-fluid">
        {this.state.alert ? alert : ""}
        {this.state.error ? error : content}

      </div>
    );
  }
}

export default App;
