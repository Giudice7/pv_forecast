function generateProductionChart(hourlyProduction) {
    Highcharts.chart('production-chart', {
        chart: {
            type: 'area',  // Change chart type to area
            backgroundColor: 'transparent', // Set transparent background color
            style: {
                fontFamily: 'Poppins, sans-serif'
            }

        },
        title: {
            text: 'Forecasting of the next 24 hours production',
            style: {
                color: 'white'  // Set the title text color to white
            }
        },
        xAxis: {
            type: 'datetime',  // Set x-axis to datetime
            labels: {
                style: {
                    color: 'white'  // Set x-axis labels color to white
                }
            },
            gridLineWidth: 0  // Remove grid lines from x-axis
        },
        yAxis: {
            title: {
                text: 'Production (kW)',
                style: {
                    color: 'white'  // Set y-axis title color to white
                }
            },
            labels: {
                style: {
                    color: 'white'  // Set y-axis labels color to white
                }
            },
            gridLineWidth: 0  // Remove grid lines from y-axis
        },
        series: [{
            name: 'Production',
            data: hourlyProduction,  // This should be in the format [timestamp, value]
            color: '#00d8ff',
            fillColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },  // Gradient fill for the area
                stops: [
                    [0, '#00d8ff'],  // Start color (same as line color)
                    [1, 'transparent']  // End color (transparent for fading effect)
                ]
            }
        }],
        legend: {
            enabled: false  // Disable the legend
        },
        credits: {
            enabled: false  // Remove the Highcharts credits text
        },
        plotOptions: {
            area: {
                marker: {
                    fillColor: '#00d8ff'  // Set marker color to the same as series color (if enabled)
                },
                dataLabels: {
                    style: {
                        color: '#00d8ff'  // Set data labels color to the same as series color
                    }
                },
                fillOpacity: 0.5  // Adjust opacity for the shaded fill
            }
        },
        tooltip: {
            xDateFormat: '%H:%M'  // Format tooltip date to show hours and minutes
        }
    });
}
