function predict_foodexp(){
    const salary=document.getElementById("salary").value
    console.log(salary)
    document.getElementById("foodexp").innerText = "predicted food expenditure " + ((salary*0.4851)+147.4)
}