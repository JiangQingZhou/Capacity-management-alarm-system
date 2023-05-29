<template>
    <div class="global">
        <el-container class="global">
            <el-header style="background-color: rgba(245, 245, 245, 0.9);">
                <el-row class="header">
                    <el-col :span="4">
                        <el-text class="title">ARIMA</el-text>
                    </el-col>
                    <el-col :span="14" v-show="isAlarm">
                        <el-button type="danger" @click="dialogVisible = true">
                            <el-icon style="right:3px">
                                <WarnTriangleFilled />
                            </el-icon>View
                        </el-button>
                    </el-col>
                    <el-col :span="14" v-show="!isAlarm"> </el-col>
                    <el-col :span="2" class="text" style="right:-42px;">数据表：</el-col>
                    <el-col :span="4">
                        <el-select v-model="value" style="height: 80px;width: 180px;" placeholder="Select" class="select" @change="changeData">
                            <el-option v-for="item in options.value" :key="item.value" :label="item.label" :value="item.value" />
                        </el-select>
                    </el-col>
                </el-row>
            </el-header>
            <el-main class="main">
                <div id="myChart" style="width:100%;height:95%;"></div>
            </el-main>
        </el-container>

        <el-dialog v-model="dialogVisible" title="Warning" draggable style="width: 700px">
            <el-table :data="alarmArr.slice((currentPage-1)*pagesize,currentPage*pagesize)" :default-sort="{ prop: 'time', order: 'descending' }" stripe max-height="300" :table-layout="auto">
                <el-table-column property="time" label="Time" sortable />
                <el-table-column property="high" label="Upper bound" />
                <el-table-column property="low" label="Lower bound" />
                <el-table-column property="value" label="Value" />
                <el-table-column property="tag" label="Tag">
                    <template #default="scope">
                        <el-tag :type="scope.row.tag === 'Higher' ? 'danger' : 'warning'">{{scope.row.tag}}</el-tag>
                    </template>
                </el-table-column>
            </el-table>
            <el-pagination layout="prev, pager, next,total" :total="total" :page-size="pagesize" @current-change="current_change"></el-pagination>
        </el-dialog>
    </div>
</template>

<script>
    // 引入echarts
    import * as echarts from 'echarts'
    import axios from "axios";
    import { ElMessage } from 'element-plus'
    import { Delete, Edit, Search, Share, Upload } from '@element-plus/icons-vue'

    export default {
        name: 'One',
        data() {
            return {
                value: '1',
                model: 'arima',
                options: [],
                number: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                alarmArr: [],
                dialogVisible: false,
                isAlarm: false,
                total: 0,//总条数
                pagesize: 10,//指定展示多少条
                currentPage: 1,//当前页码
            }
        },
        mounted() { // 需要在页面加载完毕后展示图表，这里使用Vue3的组合式生命周期钩子 onMounted()
            this.options.value = this.number.map((item) => {
                return { value: `${item}`, label: `${item}` }
            })
            console.log(this.options.value)

            this.setChart()
        },
        methods: {
            current_change(currentPage) {
                this.currentPage = currentPage;
            },
            setChart() {
                this.alarmArr = []
                this.isAlarm = false

                let myChart = echarts.init(document.getElementById("myChart"));
                this.getChart(myChart)
            },
            changeModel(label, event) {
                this.model = label.props.label.toLowerCase()
                console.log(this.model)
                this.setChart()
            },
            changeData(val) {
                console.log(this.value)
                this.setChart()
            },
            changePeriod(val) {
                console.log(this.period)
                this.setChart()
            },
            async getChart(myChart) {
                let values = 1
                let collect_time = []
                let up_values = 1
                let down_values = 1
                let origin_data = 0
                let alarm = []
                let alarmArr = []
                await axios.post('http://127.0.0.1:5000/getalarm', {
                    data: this.value,
                    model: this.model,
                }).then(function (res) {
                    values = res.data.values;
                    collect_time = res.data.collect_time;
                    up_values = res.data.up_values;
                    down_values = res.data.down_values;
                    origin_data = res.data.origin_data;
                    alarm = res.data.alarm

                    alarm.forEach((item, i) => {
                        if (alarm[i] == 'Higher' || alarm[i] == 'Lower') {
                            alarmArr.push([collect_time[i], origin_data[i]])
                        }
                    });

                    var option = {
                        title: {
                            text: '动态阈值告警'
                        },
                        tooltip: {
                            trigger: 'axis'
                        },
                        legend: {},
                        toolbox: {
                            show: true,
                            feature: {
                                dataZoom: {
                                    yAxisIndex: 'none',
                                },
                                dataView: {
                                    readOnly: true,
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
                                magicType: { type: ['line', 'bar'] },
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
                                zlevel: 1
                            },
                            {
                                name: 'Predict',
                                type: 'line',
                                data: values,
                                color: 'orange',
                                zlevel: 2
                            },
                            {
                                name: 'Lowest',
                                type: 'line',
                                data: down_values,
                                color: 'rgb(255,255,120)',
                                zlevel: 1
                            },
                            {
                                name: 'Real',
                                type: 'line',
                                data: origin_data,
                                color: 'yellowgreen',
                                zlevel: 3
                            },
                            {
                                name: 'Warning',
                                type: 'scatter',
                                data: alarmArr,
                                color: 'red',
                                zlevel: 5,
                                showSymbol: true,
                                symbol: 'circle',
                                symbolSize: 4
                            }
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
                })

                alarm.forEach((item, i) => {
                    if (alarm[i] == 'Higher' || alarm[i] == 'Lower') {
                        this.alarmArr.push({
                            time: collect_time[i],
                            value: origin_data[i],
                            high: up_values[i],
                            low: down_values[i],
                            tag: alarm[i]
                        });
                    }
                });

                if (this.alarmArr.length > 0) {
                    this.isAlarm = true
                    ElMessage({
                        message: 'Warning! There is some anomalous data in sheet' + this.value + '.',
                        type: 'warning',
                    })
                }

                this.total = this.alarmArr.length

                setTimeout(() => {
                    console.log(alarmArr)
                }, 500)
            },
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
        /* left: -40px; */
    }

    .text {
        line-height: 30px;
        font-size: 14px;
        right: -8px;
        color: black;
    }

    .title {
        font-size: 20px;
        left: 6px;
        font-weight: bold;
        line-height: 30px;
        color: black;
    }

    .header {
        top: 14px;
    }
</style>