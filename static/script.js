function dateToString(d) {
  const year = d.getFullYear();
  const month = (d.getMonth() + 1).toString().padStart(2, "0");
  const day = (d.getDate()).toString().padStart(2, "0");
  const hours = (d.getHours()).toString().padStart(2, "0");
  const minutes = (d.getMinutes()).toString().padStart(2, "0");
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}



function update_feed_times() {
  fetch('./times')
    .then(response => response.json())
    .then(data => {
      const list = document.getElementById("log");

      // Remove all children from the list
      while (list.firstChild) {
        list.removeChild(list.firstChild);
      }

      // Append each new time
      data.feed_times.forEach(time => {
        const item = document.createElement('li');
        const d = new Date(time);
        timeStr = dateToString(d);
        agoStr = ago(d.getTime());
        item.textContent = `${timeStr} (${agoStr} ago)`;
        list.appendChild(item);
      });
    })
    .catch(error => console.error('Error:', error));
}

document.onload = update_feed_times();

document.getElementById("feedButton").addEventListener("click", function() {
  fetch('./feed') // Call the endpoint to write time
    .then(() => update_feed_times())
    .catch(error => console.error('Error:', error));
});
