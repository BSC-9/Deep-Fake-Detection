// Wait for the DOM to fully load before executing the script
document.addEventListener('DOMContentLoaded', () => {
    // Get the form element by its ID
    const form = document.getElementById('celebrity-recognition-form');
  
    // Add an event listener for the form submission
    form.addEventListener('submit', async (event) => {
      // Prevent the default form submission behavior
      event.preventDefault();
  
      // Create a FormData object from the form
      const formData = new FormData(form);
  
      // Retrieve the file from the FormData
      const file = formData.get('file');
  
      // Check if a file was selected
      if (!file) {
        alert('Please select a file to upload.');
        return;
      }
  
      try {
        // Make a POST request to the server with the form data
        const response = await fetch('http://127.0.0.1:5000/recognize_celebrities', {
          method: 'POST',
          body: formData,
        });
  
        // Check if the response is successful (status code 2xx)
        if (!response.ok) {
          throw new Error('Failed to recognize celebrities.');
        }
        console.log(response.json)}
        catch(err){
            console.error(err)
            
        }
  
    });
  });
  