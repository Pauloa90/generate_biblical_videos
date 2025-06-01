name: Generate Biblical Videos

on:
  workflow_dispatch:
    inputs:
      scenes_to_generate:
        description: 'Which scenes to generate? (all/failed/specific)'
        required: true
        default: 'all'
        type: choice
        options:
          - all
          - failed
          - specific
      specific_scenes:
        description: 'If specific, enter scene IDs (comma-separated, e.g., 1,3,5)'
        required: false
        default: ''
      parallel_generation:
        description: 'Generate videos in parallel?'
        required: true
        default: true
        type: boolean

jobs:
  generate-videos:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
    
    - name: Create images directory
      run: mkdir -p images
    
    # Option 1: If images are in the repository
    # (Make sure to add your images to the repository first)
    
    # Option 2: Download images from Google Drive
    # Uncomment and modify the following section if using Google Drive
    # - name: Download images from Google Drive
    #   run: |
    #     # David.png
    #     wget -O images/David.png "https://drive.google.com/uc?export=download&id=YOUR_DAVID_FILE_ID"
    #     # Saul.png
    #     wget -O images/Saul.png "https://drive.google.com/uc?export=download&id=YOUR_SAUL_FILE_ID"
    #     # Golias.png
    #     wget -O images/Golias.png "https://drive.google.com/uc?export=download&id=YOUR_GOLIAS_FILE_ID"
    #     # Background images
    #     wget -O images/bg1.png "https://drive.google.com/uc?export=download&id=YOUR_BG1_FILE_ID"
    #     wget -O images/bg2.png "https://drive.google.com/uc?export=download&id=YOUR_BG2_FILE_ID"
    #     wget -O images/bg3.png "https://drive.google.com/uc?export=download&id=YOUR_BG3_FILE_ID"
    #     wget -O images/bg4.png "https://drive.google.com/uc?export=download&id=YOUR_BG4_FILE_ID"
    #     wget -O images/bg5.png "https://drive.google.com/uc?export=download&id=YOUR_BG5_FILE_ID"
    
    - name: Generate videos
      env:
        PIAPI_API_KEY: ${{ secrets.PIAPI_API_KEY }}
        SCENES_TO_GENERATE: ${{ github.event.inputs.scenes_to_generate }}
        SPECIFIC_SCENES: ${{ github.event.inputs.specific_scenes }}
        PARALLEL_GENERATION: ${{ github.event.inputs.parallel_generation }}
      run: |
        python generate_biblical_videos.py
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: video-generation-results
        path: |
          video_results_*.json
          *.log
    
    - name: Create summary
      if: always()
      run: |
        echo "## 🎬 Biblical Video Generation Results" >> $GITHUB_STEP_SUMMARY
        echo "" >> $GITHUB_STEP_SUMMARY
        
        # Parse results from the latest JSON file
        RESULTS_FILE=$(ls -t video_results_*.json | head -1)
        
        if [ -f "$RESULTS_FILE" ]; then
          SUCCESSFUL=$(jq -r '.successful' $RESULTS_FILE)
          FAILED=$(jq -r '.failed' $RESULTS_FILE)
          TOTAL=$(jq -r '.total_scenes' $RESULTS_FILE)
          TIME=$(jq -r '.total_time_seconds' $RESULTS_FILE)
          
          echo "### 📊 Summary" >> $GITHUB_STEP_SUMMARY
          echo "- **Total Scenes**: $TOTAL" >> $GITHUB_STEP_SUMMARY
          echo "- **✅ Successful**: $SUCCESSFUL" >> $GITHUB_STEP_SUMMARY
          echo "- **❌ Failed**: $FAILED" >> $GITHUB_STEP_SUMMARY
          echo "- **⏱️ Total Time**: ${TIME}s" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          
          # List successful videos
          echo "### ✅ Generated Videos" >> $GITHUB_STEP_SUMMARY
          jq -r '.results[] | select(.status == "completed") | "- **Scene \(.scene_id)** - \(.scene_name): [\(.video_url)](\(.video_url))"' $RESULTS_FILE >> $GITHUB_STEP_SUMMARY
          
          # List failed scenes
          if [ "$FAILED" -gt 0 ]; then
            echo "" >> $GITHUB_STEP_SUMMARY
            echo "### ❌ Failed Scenes" >> $GITHUB_STEP_SUMMARY
            jq -r '.results[] | select(.status == "failed") | "- **Scene \(.scene_id)** - \(.scene_name): \(.error)"' $RESULTS_FILE >> $GITHUB_STEP_SUMMARY
          fi
        else
          echo "❌ No results file found!" >> $GITHUB_STEP_SUMMARY
        fi
    
    # Optional: Save videos to Google Drive
    # - name: Upload videos to Google Drive
    #   if: success()
    #   uses: adityak74/google-drive-upload-action@main
    #   with:
    #     credentials: ${{ secrets.GDRIVE_CREDENTIALS }}
    #     filename: "video_results_*.json"
    #     folderId: ${{ secrets.GDRIVE_FOLDER_ID }}
    
    # Optional: Send notification
    # - name: Send notification
    #   if: always()
    #   run: |
    #     # Add your notification logic here (Slack, Email, etc.)
    #     echo "Video generation completed!"
