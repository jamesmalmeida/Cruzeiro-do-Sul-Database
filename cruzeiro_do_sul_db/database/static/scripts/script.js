window.onload = SearchMethodCheck();

function SearchMethodCheck() {
  x = document.getElementById("SelectSearch");
  if (x) {
    if (x.value == "Comparation") {
      document.getElementById("ComparationEnergyLegend").style.display = "block";
      document.getElementById("ComparationEnergyFile").style.display = "block";
      document.getElementById("ComparationMuLegend").style.display = "block";
      document.getElementById("ComparationMuFile").style.display = "block";
    }
    else {
      document.getElementById("ComparationEnergyLegend").style.display = "none";
      document.getElementById("ComparationEnergyFile").style.display = "none";
      document.getElementById("ComparationMuLegend").style.display = "none";
      document.getElementById("ComparationMuFile").style.display = "none";
    }
  }
}

function AddElement(string) {
  x = document.getElementById("absorbing_element")
  y = document.getElementById("composition");
  if (x) {
    x.value += string + ' ';
  }
  if (y) {
    y.value += string + ' ';
  }
}