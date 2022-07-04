google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
  var data = google.visualization.arrayToDataTable([
    ["Type", "Value"],
    ["Purchased raw materials", parseInt(selectedPurchasedMaterials)],
    ["Sold raw materials", Math.abs(selectedSoldMaterials)],
  ]);

  var options = {
    is3D: true,
    fontSize: 20,
  };

  var chart = new google.visualization.PieChart(
    document.getElementById("piechart_3d")
  );
  chart.draw(data, options);
}
