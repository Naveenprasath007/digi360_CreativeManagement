// var options = {
//     series: [{
//     data: [21, 22, 10, 28, 16, 21]
//   }],
//     chart: {
//     height: 200,
//     type: 'bar',
//     events: {
//       click: function(chart, w, e) {
//         // console.log(chart, w, e)
//       }
//     }
//   },
//   colors: ['#60E19C', '#F37086', '#81D1FF', '#574AAB', '#61FF00', '#9A9E9C'],
//   plotOptions: {
//     bar: {
//       columnWidth: '45%',
//       distributed: true,
//     }
//   },
//   dataLabels: { 
//     enabled: false
//   },
//   legend: {
//     show: false
//   },
//   xaxis: {
//     categories: [
//       'AVI',
//       'MP4',
//       'WMV',
//       'JPG',
//       'PNG',
//       'GIF' 
//     ],
//     labels: {
//       style: {
//         colors: ['#60E19C', '#F37086', '#81D1FF', '#574AAB', '#61FF00', '#9A9E9C'],
//         fontSize: '12px'
//       }
//     }
//   }
//   };

//   var chart = new ApexCharts(document.querySelector("#barChart"), options);
//   chart.render();

//   var optionsArea = {
//     series: [{
//     name: 'series1',
//     data: [31, 40, 28, 51, 42, 109, 100]
//   }, {
//     name: 'series2',
//     data: [11, 32, 45, 32, 34, 52, 41]
//   }],
//     chart: {
//     height: 350,
//     type: 'area'
//   },
//   dataLabels: {
//     enabled: false
//   },
//   stroke: {
//     curve: 'smooth'
//   },
//   xaxis: {
//     type: 'datetime',
//     categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
//   },
//   tooltip: {
//     x: {
//       format: 'dd/MM/yy HH:mm'
//     },
//   },
//   };

//   var chart = new ApexCharts(document.querySelector("#uploadHistory"), optionsArea);
//   chart.render();


// LIST GRID
function showList(e) {
  var $gridCont = $('.grid-container');
  e.preventDefault();
  $gridCont.hasClass('list-view') ? $gridCont.removeClass('list-view') : $gridCont.addClass('list-view');
}
function gridList(e) {
  var $gridCont = $('.grid-container')
  e.preventDefault();
  $gridCont.removeClass('list-view');
}

$(document).on('click', '.btn-grid', gridList);
$(document).on('click', '.btn-list', showList);



function myFunction() {
  var element = document.getElementById("accountSection");
  element.classList.toggle("active");
}


$('.message').hide().fadeIn(500).delay(2000).fadeOut(500);  
