// Initialize Firebase
const config = {
  apiKey: "AIzaSyBt1rN2oz9WSsb-t_z1RIw9PBslHGuEwZM",
  authDomain: "pi-server-cc2b0.firebaseapp.com",
  databaseURL: "https://pi-server-cc2b0.firebaseio.com",
  projectId: "pi-server-cc2b0",
  storageBucket: "pi-server-cc2b0.appspot.com",
  messagingSenderId: "544520465241"
};
firebase.initializeApp(config);

// Init database
const db = firebase.firestore()

// Collect DOM to add data
const envTable = document.querySelector('#sensorValues')
const colorBox = document.querySelector('#colorBox')

// On update: update values in table
db.collection('pi').doc('environment')
  .onSnapshot((doc) => {
    sensorData = doc.data()
    console.log(sensorData)
    envTable.innerHTML = ''
    sensors = Object.keys(sensorData)
    sensorVals = Object.values(sensorData)
    sensors.forEach((sensor, i) => {
      envTable.innerHTML += `
        <tr>
          <td>${sensor.toUpperCase()}</td>
          <td>${sensorVals[i].value}</td>
          <td>${sensorVals[i].unit}</td>
        </tr>
      `
    });

  })

// Form fields to change SenseHat
const colorTextField = document.querySelector('#color_text')
const colorPicker = document.querySelector('#color_picker')
const colorCheckBox = document.querySelector('#color_on_off')

// Update db color with value
const updateState = (state) => {
  db.collection('pi').doc('color').set({
    state: state,
  }, {merge: true})
}

const updateColor = (color) => {
  db.collection('pi').doc('color').set({
    value: color
  }, {merge: true})
}

const updateColorBox = (color) => {
  colorBox.style.background = color
}

// Enable/Disable colour fields depending on checkbox
// Also update db with on/off state
colorCheckBox.addEventListener('change', () => {
  if(colorCheckBox.checked) {
    console.log('checked')
    colorTextField.removeAttribute('disabled')
    colorPicker.removeAttribute('disabled')
    updateState('on')
  } else {
    console.log('unchecked')
    colorTextField.setAttribute('disabled', 'disabled')
    colorPicker.setAttribute('disabled', 'disabled')
    updateState('off')
  }
})

colorTextField.addEventListener('change', () => {
  color = colorTextField.value
  colorPicker.value = color
  updateColor(color)
  updateColorBox(color)
})

colorPicker.addEventListener('change', () => {
  color = colorPicker.value
  colorTextField.value = color
  updateColor(color)
  updateColorBox(color)
})