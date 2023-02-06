window.onload = SearchMethodCheck();

function SearchMethodCheck() {
  if (document.getElementById("SelectSearch").value == "Comparation") {
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

function ButtonClickAddElement(string) {
  document.getElementById("absorbing_element").value = string;
  document.getElementById("composition").value = string;
}
