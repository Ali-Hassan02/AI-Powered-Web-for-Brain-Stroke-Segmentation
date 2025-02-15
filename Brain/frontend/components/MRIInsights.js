import { useState } from "react";
import ResultSection from "./ResultSection";

const MRIInsights = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imageSlices, setImageSlices] = useState([]);
  const [segmentationSlices, setSegmentationSlices] = useState([]);
  const [currentSlice, setCurrentSlice] = useState(0);
  const [loading, setLoading] = useState(false); // New loading state
  const [start , setStart] = useState(false)
  const handleFileChange = (event) => {
    setStart(true)
    const file = event.target.files[0];

    if (file) {
      if (!file.name.endsWith(".nii.gz")) {
        alert("Invalid file type. Please upload a .nii.gz file.");
        event.target.value = "";
        return;
      }

      setSelectedFile(file.name);
      setLoading(true); // Start the loader

      // Create FormData object to send the file
      const formData = new FormData();
      formData.append("file", file);

      // Send the file to Flask backend
      fetch("http://localhost:5001/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            alert(`Error: ${data.error}`);
            setLoading(false); // Stop the loader
            return;
          }

          setImageSlices(data.image_3d); // Array of image slices
          setSegmentationSlices(data.segmentation_3d); // Array of segmentation slices
          setCurrentSlice(0); // Reset to the first slice
          setLoading(false); // Stop the loader
        })
        .catch((error) => {
          console.error("Error:", error);
          setLoading(false); // Stop the loader
        });
    }
  };

  const handleNextSlice = () => {
    if (currentSlice < imageSlices.length - 1) {
      setCurrentSlice(currentSlice + 1);
    }
  };

  const handlePrevSlice = () => {
    if (currentSlice > 0) {
      setCurrentSlice(currentSlice - 1);
    }
  };

  return (
    <div className="w-full flex flex-col lg:flex-row h-screen">
      {/* Sidebar */}
      <div className="bg-indigo-100 w-full lg:w-1/3 p-8 text-center shadow-md flex flex-col justify-center items-center">
        <div className="mb-6">
          <img src="/brain-organic.svg" alt="Brain Icon" className="w-30" />
        </div>
        <h1 className="text-5xl font-semibold text-gray-700">BRAIN</h1>
        <p className="text-3xl font-semibold text-orange-600">
          AI-Powered, MRI Insights
        </p>
        <p className="text-xl text-gray-600">for Better Health Care</p>
      </div>

      {/* Main Content */}
      <div className="w-full lg:w-4/5 p-8 lg:p-12 overflow-y-auto">
        <div className="flex flex-col items-center ">
          <h1 className="text-3xl sm:text-4xl mb-6 text-gray-800">
            Get MRI Details
          </h1>
          <label className="block text-lg sm:text-xl text-gray-600 mb-4">
            Please Upload .nii.gz format brain scan
          </label>
          {/* File Upload */}
          <div className="flex flex-col items-center mb-6">
            <label
              htmlFor="file-upload"
              className="bg-blue-500 text-white px-6 py-3 rounded-lg cursor-pointer text-lg"
            >
              Choose File
              <input
                type="file"
                id="file-upload"
                className="hidden"
                accept=".nii.gz"
                onChange={handleFileChange}
              />
            </label>

            <span className="mt-2 text-gray-500">
              {selectedFile ? selectedFile : "No File Chosen"}
            </span>
          </div>
          {/* Results Section */}
          {start ? (
          <ResultSection
            imageSlices={imageSlices}
            segmentationSlices={segmentationSlices}
            currentSlice={currentSlice}
            handleNextSlice={handleNextSlice}
            handlePrevSlice={handlePrevSlice}
            loading={loading} // Pass loading state to the child
          />
          ) : (
          <div className="flex justify-center items-center h-[400px]">
            <img
              src="/brain_icon.png"
              alt="Brain Placeholder"
              className="w-64 h-auto"
            />
          </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MRIInsights;