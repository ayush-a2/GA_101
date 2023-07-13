// Constants
const classLabels = ["fruit", "book"]; // Class labels for fruit and book
const numClasses = classLabels.length; // Number of classes
const numExamples = 5; // Number of examples to train per class

// Load the Teachable Machine model
async function loadModel() {
  const URL = 'https://teachablemachine.withgoogle.com/models/bXy2kDNi/';
  // Replace with your model URL
  const model = await knn.load();
  return model;
}

// Initialize the webcam and start object classification
async function init() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const resultDiv = document.getElementById('result');
  const model = await loadModel();

  const classifier = knn.create();
  const webcam = await tf.data.webcam(video);

  // Train the model with example images
  for (let i = 0; i < numExamples; i++) {
    const img = await webcam.capture();
    const activation = model.infer(img, 'conv_preds');
    classifier.addExample(activation, i % numClasses);
    img.dispose();
    await tf.nextFrame();
  }

  setInterval(async () => {
    if (classifier.getNumClasses() > 0) {
      const img = await webcam.capture();
      const activation = model.infer(img, 'conv_preds');
      const result = await classifier.predictClass(activation);

      const className = classLabels[result.label];
      const probability = result.confidences[result.label].toFixed(2);

      resultDiv.innerHTML = `Object: ${className}<br>Confidence: ${probability}`;

      handleObjectClassification(className, resultDiv);

      img.dispose();
    }

    await tf.nextFrame();
  }, 1000);
}

// Handle object classification
function handleObjectClassification(className, resultDiv) {
  if (className === 'fruit') {
    handleFruitClassification(resultDiv);
  } else if (className === 'book') {
    handleBookClassification(resultDiv);
  }
}

// Handle fruit classification
function handleFruitClassification(resultDiv) {
  // Replace with your custom logic to handle fruit classification

  // Simulating a delay to fetch fruit information
  setTimeout(() => {
    const fruitName = "Apple";
    const nutritionalValues = {
      calories: 52,
      carbohydrates: 14,
      fiber: 2.4,
      vitamins: ["A", "C"],
    };

    const fruitInfoHTML = `
      <h2>${fruitName}</h2>
      <p>Calories: ${nutritionalValues.calories}</p>
      <p>Carbohydrates: ${nutritionalValues.carbohydrates}g</p>
      <p>Fiber: ${nutritionalValues.fiber}g</p>
      <p>Vitamins: ${nutritionalValues.vitamins.join(", ")}</p>
    `;

    resultDiv.innerHTML = fruitInfoHTML;
  }, 2000);
}

// Handle book classification
function handleBookClassification(resultDiv) {
  // Replace with your custom logic to handle book classification

  // Simulating a delay to fetch book information
  setTimeout(() => {
    const bookTitle = "Example Book";
    const bookInfo = {
      author: "John Doe",
      publisher: "Example Publisher",
      publicationYear: 2023,
      summary: "This is an example book about a topic.",
    };

    const bookInfoHTML = `
      <h2>${bookTitle}</h2>
      <p>Author: ${bookInfo.author}</p>
      <p>Publisher: ${bookInfo.publisher}</p>
      <p>Publication Year: ${bookInfo.publicationYear}</p>
      <p>Summary: ${bookInfo.summary}</p>
    `;

    resultDiv.innerHTML = bookInfoHTML;
  }, 2000);
}

// Start the application
init();
