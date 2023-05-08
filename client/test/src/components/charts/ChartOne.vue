<template>
    <div class="global">
        <el-container class="global">
            <el-header style="background-color: rgba(245, 245, 245, 0.9);">
                <el-row class="header">
                    <el-col :span="12">
                        <el-tabs stretch style="height: 80px;width: 360px;" class="demo-tabs" @tab-click="changeModel">
                            <el-tab-pane label="CNN"></el-tab-pane>
                            <!-- <el-tab-pane label="RNN"></el-tab-pane> -->
                            <el-tab-pane label="LSTM"></el-tab-pane>
                            <el-tab-pane label="ARIMA"></el-tab-pane>
                        </el-tabs>
                    </el-col>
                    <el-col :span="2" class="text" style="right:-42px;">数据表：</el-col>
                    <el-col :span="4">
                        <el-select v-model="value" style="height: 80px;width: 180px;" placeholder="Select" class="select" @change="changeData">
                            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </el-col>
                    <el-col :span="2" class="text">预测周期(天)：</el-col>
                    <el-col :span="4">
                        <el-select v-model="period" style="height: 80px;width: 180px;" placeholder="Select" class="select" @change="changePeriod">
                            <el-option v-for="item in periodOpt" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </el-col>
                </el-row>
            </el-header>
            <el-main class="main">
                <div id="myChart" style="width:100%;height:95%;"></div>
            </el-main>
        </el-container>
    </div>
</template>

<script>
    // 引入echarts
    import * as echarts from 'echarts'
    import axios from "axios";

    export default {
        name: 'One',
        data() {
            return {
                value: '1',
                period: '100',
                model: 'cnn',
                options: [
                    {
                        value: '1',
                        label: 'test-aiops-hbase-203',
                    },
                    {
                        value: '2',
                        label: 'test-bpfp-bs-engine2-ft',
                    },
                    {
                        value: '3',
                        label: 'test-rr_offline_qf_cluster',
                    }
                ],
                periodOpt: [
                    {
                        value: '100',
                        label: '100',
                    },
                    {
                        value: '200',
                        label: '200',
                    },
                    {
                        value: '300',
                        label: '300',
                    }
                ]
            }
        },
        mounted() { // 需要在页面加载完毕后展示图表，这里使用Vue3的组合式生命周期钩子 onMounted()
            let myChart = echarts.init(document.getElementById("myChart"));
            this.getChart(myChart)
        },
        methods: {
            changeModel(label, event) {
                let myChart = echarts.init(document.getElementById("myChart"));
                this.model = label.props.label.toLowerCase()
                console.log(this.model)
                this.getChart(myChart)
            },
            changeData(val) {
                let myChart = echarts.init(document.getElementById("myChart"));
                console.log(this.value)
                this.getChart(myChart)
            },
            changePeriod(val) {
                let myChart = echarts.init(document.getElementById("myChart"));
                console.log(this.period)
                this.getChart(myChart)
            },
            getChart(myChart) {
                let values = 1
                let collect_time = []
                let up_values = 1
                let down_values = 1
                let origin_data = 0
                axios.post('http://127.0.0.1:5000/getchart', {
                    data: this.value,
                    model: this.model,
                    period: this.period
                }).then(function (res) {
                    values = res.data.values;
                    collect_time = res.data.collect_time;
                    up_values = res.data.up_values;
                    down_values = res.data.down_values;
                    origin_data = res.data.origin_data;

                    let end = collect_time[origin_data.length - 1]
                    let str = origin_data[origin_data.length - 1]

                    var option = {
                        title: {
                            text: '容量管理算法模型'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {},
                        toolbox: {
                            show: true,
                            feature: {
                                dataZoom: {
                                    yAxisIndex: 'none'
                                },
                                dataView: {
                                    optionToContent: function (opt) {
                                        var axisData = opt.xAxis[0].data;
                                        var series = opt.series;
                                        var table = '<table style="width:100%;text-align:center"><tbody><tr>' +
                                            "<td>时间</td>" + "<td>" + series[0].name + "</td>" + "<td>" + series[1].name + "</td>" +
                                            "<td>" + series[2].name + "</td>" + "<td>" + series[3].name + "</td>" + "</tr>"
                                        for (var i = 0, l = axisData.length; i < l; i++) {
                                            table += "<tr>" + "<td>" + axisData[i] + "</td>" +
                                                "<td>" + series[0].data[i] + "</td>" +
                                                "<td>" + series[1].data[i] + "</td>" + "<td>" + series[2].data[i] + "</td>" +
                                                "<td>" + series[3].data[i] + "</td>" + "</tr>";
                                        }
                                        table += "</tbody></table>";
                                        return table;
                                    }
                                },
                                magicType: { type: ['line', 'bar', 'stack'] },
                                saveAsImage: {}
                            }
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: collect_time
                        },
                        yAxis: {
                            type: 'value',
                            scale: true,
                            axisLabel: {
                                interval: 0,
                                rotate: 35,
                                formatter: '{value}'
                            }
                        },
                        series: [
                            {
                                name: 'Highest',
                                type: 'line',
                                data: up_values,
                                color: 'rgb(255,255,120)',
                            },
                            {
                                name: 'Predict',
                                type: 'line',
                                data: values,
                                color: 'orange',
                                markLine: {
                                    lineStyle: {
                                        width: 2,
                                        color: 'grey',
                                    },
                                    label: {
                                        show: true,
                                        position: 'end',
                                        formatter: 'Real',
                                        color: 'black',
                                        height: 10,
                                        padding: [12, 12, 7, 12],
                                        lineHeight: 10,
                                        fontWeight: 550,
                                    },
                                    silent: true, // 鼠标悬停事件, true悬停不会出现实线
                                    symbol: 'none', // 去掉箭头
                                    data: [[
                                        { coord: [end, 0] }, // [x第几个（从0开始），y轴起始点 ]
                                        { coord: [end, str] }
                                    ]]
                                }
                            },
                            {
                                name: 'Lowest',
                                type: 'line',
                                data: down_values,
                                color: 'rgb(255,255,120)',
                            },
                            {
                                name: 'Real',
                                type: 'line',
                                data: origin_data,
                                color: 'yellowgreen',
                            },
                        ]
                    }
                    myChart.setOption(option);
                    window.onresize = function () {
                        setTimeout(function () {
                            myChart.resize()
                        }, 10)
                    }
                }).catch(err => {
                    console.log('123')
                });
            }
        }
    }
</script>

<style scoped>
    .global {
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: 0;
        padding: 0;
        height: 100%;
        width: 100%;
        position: relative;
    }

    .select {
        top: 10px;
        /* left: -40px; */
    }

    .text {
        line-height: 30px;
        font-size: 14px;
        top: 10px;
        right: -8px;
        color: black;
    }

    .header {
        top: 6px;
    }

    .demo-tabs {
        top: 2px;
    }
</style>