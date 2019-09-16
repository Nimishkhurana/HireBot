/*
*  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
*
*  Use of this source code is governed by a BSD-style license
*  that can be found in the LICENSE file in the root of the source
*  tree.
*/

// This code is adapted from
// https://rawgit.com/Miguelao/demos/master/mediarecorder.html

'use strict';

/* globals MediaRecorder */

var mediaSource;

let mediaRecorder;
let recordedBlobs;
let sourceBuffer;

var errorMsgElement;
var recordedVideo;
var recordButton;
var infoText;


console.log("Before loading")
window.addEventListener('load',()=>{
    console.log("In loading1")
    counter_();
    setTimeout(startCamera,30000);
    console.log("In loading")
    mediaSource = new MediaSource();
    console.log("Before event listener")
    errorMsgElement = document.querySelector('span#errorMsg');
    recordedVideo = document.querySelector('video#recorded');
    recordButton = document.querySelector('button#record');
    recordButton.addEventListener("click",stopRecording);
    mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
    console.log("loading completed")
});


// Update the count down every 1 second
function counter_(){
    var count1 = 150
    var x = setInterval(function () {

    if (count1 < 1) {
        clearInterval(x);
        stopRecording();
        
    }
      
    document.getElementById("demo").innerHTML = count1-- + "s";   
      }, 1000);
}



function handleSourceOpen(event) {
  console.log('MediaSource opened');
  sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
  console.log('Source buffer: ', sourceBuffer);
}

function handleDataAvailable(event) {
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}

function startRecording() {
  
  console.log("StartRecording called");
  recordedBlobs = [];
  let options = { mimeType: 'video/webm;codecs=vp9' };
  if (!MediaRecorder.isTypeSupported(options.mimeType)) {
    console.error(`${options.mimeType} is not Supported`);
    errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
    options = { mimeType: 'video/webm;codecs=vp8' };
    if (!MediaRecorder.isTypeSupported(options.mimeType)) {
      console.error(`${options.mimeType} is not Supported`);
      errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
      options = { mimeType: 'video/webm' };
      if (!MediaRecorder.isTypeSupported(options.mimeType)) {
        console.error(`${options.mimeType} is not Supported`);
        errorMsgElement.innerHTML = `${options.mimeType} is not Supported`;
        options = { mimeType: '' };
      }
    }
  }

  try {
    mediaRecorder = new MediaRecorder(window.stream, options);
  } catch (e) {
    console.error('Exception while creating MediaRecorder:', e);
    errorMsgElement.innerHTML = `Exception while creating MediaRecorder: ${JSON.stringify(e)}`;
    return;
  }

  console.log('Created MediaRecorder', mediaRecorder, 'with options', options);
  mediaRecorder.onstop = (event) => {

    console.log('Recorder stopped: ', event);
  };

  mediaRecorder.ondataavailable = handleDataAvailable;
  mediaRecorder.start(10); // collect 10ms of data
  console.log('MediaRecorder started', mediaRecorder);
}

function stopRecording() {
  console.log("Stopped fucntion")
  mediaRecorder.stop();
  console.log('Recorded Blobs: ', recordedBlobs);
  const blob = new Blob(recordedBlobs, { type: 'video/webm' });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = 'test.webm';
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }, 100);
}


function handleSuccess(stream) {
  recordButton.disabled = false;
  console.log('getUserMedia() got stream:', stream);
  window.stream = stream;

  const gumVideo = document.querySelector('video#gum');
  gumVideo.srcObject = stream;
}

async function init(constraints) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
  } catch (e) {
    console.error('navigator.getUserMedia error:', e);
    errorMsgElement.innerHTML = `navigator.getUserMedia error:${e.toString()}`;
  }
}


  async function startCamera() {
    infoText = document.querySelector('#info');
    infoText.innerHTML = "Recording Started";
    const hasEchoCancellation = document.querySelector('#echoCancellation').checked;
    const constraints = {
        audio: {
        echoCancellation: { exact: hasEchoCancellation }
        },
        video: {
        width: 1280, height: 720
        }
    };
    console.log('Using media constraints:', constraints);
    await init(constraints);
    startRecording();
}
