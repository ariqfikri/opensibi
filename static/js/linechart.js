
$(document).ready(function() {
  $.ajax({
      url: '/monitor',
      type: 'GET',
      dataType: 'json',
      success: function(data, textStatus, xhr) {
        console.log(data)
        let categories = []
        data.myo.map((v) => {
          categories.push(v.tanggal)
        })
        data.leap.map((v) => {
          categories.push(v.tanggal)
        })
        data.voice.map((v) => {
          categories.push(v.tanggal)
        })
        categories = [... new Set(categories)]
        console.log(data.voice.map((v) => {
          return v.total;
        }))
        var options = {
          chart: {
            height: 350,
            type: "line",
            stacked: false
          },
          dataLabels: {
            enabled: true
          },
          colors: ["#03a60b", "#ffc516", "#ff1616"],
          series: [
            {
              name: "Leap Service",
              data: data.leap.map((v) => {
                return v.total;
              })
            },
            {
              name: "Myo Service",
              data: data.myo.map((v) => {
                return v.total;
              })
            },
            {
              name: "Voice Service",
              data: data.voice.map((v) => {
                return v.total;
              })
            }
          ],
          stroke: {
            width: [4, 4, 4]
          },
          plotOptions: {
            bar: {
              columnWidth: "20%"
            }
          },
          xaxis: {
            categories: categories,
          },
          yaxis: [
            {
              axisTicks: {
                show: true
              },
              axisBorder: {
                show: true,
                color: "#247BA0"
              },
              labels: {
                style: {
                  colors: "#247BA0"
                }
              },
            }
          ],
          tooltip: {
            shared: false,
            intersect: true,
            x: {
              show: false
            }
          },
          legend: {
            horizontalAlign: "left",
            offsetX: 40
          }
        };
        
        var chart = new ApexCharts(document.querySelector("#chart"), options);
        
        chart.render();  
        
      },  
      error: function(xhr, textStatus, errorThrown) {  
          console.log('Error in Database');  
      }  
  });  
});  

  