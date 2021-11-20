const foodBalanceWrapper = document.getElementById("foodBalanceWrapper")
foodBalanceWrapper.style.display = "none";

// provided: vanilla JS autocomplete
// https://goodies.pixabay.com/javascript/auto-complete/demo.html
new autoComplete({
  selector: 'input[name="foodPicker"]',
  minChars: 2,
  source: function(term, suggest){
    term = term.toLowerCase();
    let choices = Object.keys(foodDb);  // defined in food.js
    let matches = [];
    for(i=0; i<choices.length; i++){
      let kcal = foodDb[choices[i]];
      if(kcal == 0){
        continue;
      }

      if(~choices[i].toLowerCase().indexOf(term)){
        let item = `${choices[i]} (${kcal} kcal)`;
        matches.push(item);
      }
    }
    suggest(matches);
  }
});


// provided: handle form submission to not do it as inline JS
// https://stackoverflow.com/a/5384732
function processForm(e) {
    console.log("form submission");
    if (e.preventDefault) e.preventDefault();
    updateFoodLog();
    return false;
}
var form = document.getElementById('foodPickerForm');
if (form.attachEvent) {
    form.attachEvent("submit", processForm);
} else {
    form.addEventListener("submit", processForm);
}


// helpers
function recalculateTotal(){
  // get all table cells (tds) and sum the calories = td with kcal
  kCalValues
}

function updateTotalKcal(){
  // write the total kcal count into  the total id, if 0 hide the
  // foodBalanceWrapper div
  foodBalanceWrapper.style.display = "block";
}

function emptyFoodPicker(){
  // reset the foodPicker ID value
}

function removeRow(){
  // remove a table row and update the total kcal
  // https://stackoverflow.com/a/53085148

  // event.target will be the input element.
  let td = event.target.parentNode; 
  let tr = td.parentNode; // the row to be removed
  tr.parentNode.removeChild(tr);
}

function updateFoodLog(){
  // udate the food table with the new food, building up the inner dom
  // elements, including adding a delete button / onclick handler
  // finally call updateTotalKcal and emptyFoodPicker
  console.log("Updating food log");
  let foodLog = document.getElementById('foodBalanceBody');

  let newFoodEntry = document.createElement('tr');

  let col1 = document.createElement('td');
  let col2 = document.createElement('td');
  let col3 = document.createElement('td');

  col1.textContent = "Sushi";
  col1.className = "food";

  col2.textContent = 500;
  col2.className = "kCal";

  let dltBtn = document.createElement("input");
  dltBtn.onclick = removeRow;
  dltBtn.type = "button";
  dltBtn.className = "delete";
  col3.appendChild(dltBtn);

  newFoodEntry.appendChild(col1);
  newFoodEntry.appendChild(col2);
  newFoodEntry.appendChild(col3);

  foodLog.appendChild(newFoodEntry);
  
  updateTotalKcal();

}
