// =============================================================================
// Jenkinsfile — Declarative Pipeline for Iris Flower ML Project
// =============================================================================
// Repo layout:
//   ML_LAB/                        ← git repo root (this file lives here)
//   ├── Jenkinsfile
//   └── iris-flower-ci/
//       ├── train.py
//       ├── predict.py
//       ├── test_model.py
//       ├── requirements.txt
//       ├── Dockerfile
//       ├── entrypoint.sh
//       └── .dockerignore
//
// Pipeline stages:
//   1  Checkout              — clone repo onto the agent
//   2  Setup Virtual Env     — create isolated Python venv
//   3  Install Dependencies  — pip install requirements + flake8
//   4  Code Quality Check    — flake8 lint report
//   5  Run Unit Tests        — pytest with JUnit XML report
//   6  Train ML Model        — python train.py (produces iris_model.pkl)
//   7  Verify Model Artifact — confirm iris_model.pkl exists
//   8  Archive Artifacts     — store model + reports in Jenkins
//   9  Build Docker Image    — docker build from iris-flower-ci/
//   10 Deploy Container      — remove old container, start new one
//   11 Container Logs        — print container output to Jenkins log
// =============================================================================

pipeline {

    // ── Agent ─────────────────────────────────────────────────────────────────
    agent any

    // ── Global environment variables ──────────────────────────────────────────
    environment {
        PROJECT_DIR    = 'iris-flower-ci'
        VENV_DIR       = "${WORKSPACE}\\${PROJECT_DIR}\\venv"
        MODEL_FILE     = 'iris_model.pkl'
        REPORTS_DIR    = "${WORKSPACE}\\${PROJECT_DIR}\\reports"
        MIN_ACCURACY   = '0.90'

        // Docker-specific variables
        // IMAGE_NAME  : name:tag used for the Docker image.
        //   BUILD_NUMBER is Jenkins' auto-incrementing build counter — using it
        //   as the tag means every build produces a uniquely tagged image,
        //   enabling rollback to any previous build.
        IMAGE_NAME     = "iris-flower:${BUILD_NUMBER}"

        // IMAGE_LATEST : a floating 'latest' tag always pointing to the newest build.
        //   Useful for pulling the current image without knowing the build number.
        IMAGE_LATEST   = 'iris-flower:latest'

        // CONTAINER_NAME : fixed name for the running container.
        //   Using a fixed name makes stop/remove/log commands predictable.
        CONTAINER_NAME = 'iris-flower-container'
    }

    // ── Pipeline-wide options ─────────────────────────────────────────────────
    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    // =========================================================================
    // STAGES
    // =========================================================================
    stages {

        // ── Stage 1: Checkout ─────────────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 1 — Checkout source code'
                echo '─────────────────────────────────────────'
                checkout scm
                echo "Workspace : ${WORKSPACE}"
                echo "Branch    : ${GIT_BRANCH}"
                echo "Commit    : ${GIT_COMMIT}"
            }
        }

        // ── Stage 2: Setup Virtual Environment ────────────────────────────────
        stage('Setup Virtual Environment') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 2 — Create Python virtual environment'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            cd ${PROJECT_DIR}
                            python3 --version
                            python3 -m venv venv
                            echo 'Virtual environment created (Unix)'
                        """
                    } else {
                        bat """
                            cd ${PROJECT_DIR}
                            python --version
                            python -m venv venv
                            echo Virtual environment created (Windows)
                        """
                    }
                }
            }
        }

        // ── Stage 3: Install Dependencies ─────────────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 3 — Install dependencies'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            cd ${PROJECT_DIR}
                            . venv/bin/activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install flake8
                            echo '--- Installed packages ---'
                            pip list
                        """
                    } else {
                        bat """
                            cd ${PROJECT_DIR}
                            call venv\\Scripts\\activate
                            pip install --upgrade pip
                            pip install -r requirements.txt
                            pip install flake8
                            echo --- Installed packages ---
                            pip list
                        """
                    }
                }
            }
        }

        // ── Stage 4: Code Quality — flake8 ────────────────────────────────────
        stage('Code Quality Check') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 4 — Code quality (flake8)'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            cd ${PROJECT_DIR}
                            . venv/bin/activate
                            flake8 . --exclude=venv \
                                     --max-line-length=120 \
                                     --statistics \
                                     --exit-zero
                        """
                    } else {
                        bat """
                            cd ${PROJECT_DIR}
                            call venv\\Scripts\\activate
                            flake8 . --exclude=venv ^
                                     --max-line-length=120 ^
                                     --statistics ^
                                     --exit-zero
                        """
                    }
                }
            }
        }

        // ── Stage 5: Unit Tests — pytest ──────────────────────────────────────
        stage('Run Unit Tests') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 5 — Unit tests (pytest)'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            cd ${PROJECT_DIR}
                            mkdir -p reports
                            . venv/bin/activate
                            python -m pytest test_model.py \
                                -v -s \
                                --junitxml=reports/test-results.xml
                        """
                    } else {
                        bat """
                            cd ${PROJECT_DIR}
                            if not exist reports mkdir reports
                            call venv\\Scripts\\activate
                            python -m pytest test_model.py ^
                                -v -s ^
                                --junitxml=reports\\test-results.xml
                        """
                    }
                }
            }
            post {
                always {
                    junit "${PROJECT_DIR}/reports/test-results.xml"
                }
            }
        }

        // ── Stage 6: Train ML Model ───────────────────────────────────────────
        stage('Train ML Model') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 6 — Train ML model (train.py)'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            cd ${PROJECT_DIR}
                            . venv/bin/activate
                            python train.py
                        """
                    } else {
                        bat """
                            cd ${PROJECT_DIR}
                            call venv\\Scripts\\activate
                            python train.py
                        """
                    }
                }
            }
        }

        // ── Stage 7: Verify Model Artifact ────────────────────────────────────
        stage('Verify Model Artifact') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 7 — Verify model artifact exists'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            if [ -f "${PROJECT_DIR}/${MODEL_FILE}" ]; then
                                echo "SUCCESS: ${MODEL_FILE} found."
                                ls -lh "${PROJECT_DIR}/${MODEL_FILE}"
                            else
                                echo "ERROR: ${MODEL_FILE} was NOT created by train.py"
                                exit 1
                            fi
                        """
                    } else {
                        bat """
                            if exist "${PROJECT_DIR}\\${MODEL_FILE}" (
                                echo SUCCESS: %MODEL_FILE% found.
                            ) else (
                                echo ERROR: %MODEL_FILE% was NOT created by train.py
                                exit /b 1
                            )
                        """
                    }
                }
            }
        }

        // ── Stage 8: Archive Artifacts ────────────────────────────────────────
        stage('Archive Artifacts') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 8 — Archive artifacts in Jenkins'
                echo '─────────────────────────────────────────'
                archiveArtifacts(
                    artifacts: "${PROJECT_DIR}/${MODEL_FILE}, ${PROJECT_DIR}/reports/**/*",
                    fingerprint: true,
                    allowEmptyArchive: false
                )
                echo "Artifacts archived: ${MODEL_FILE} + test reports"
            }
        }

        // ── Stage 9: Build Docker Image ───────────────────────────────────────
        // Runs AFTER all tests pass so we only build an image from verified code.
        //
        // `docker build` flags used:
        //   -t ${IMAGE_NAME}   : tag as iris-flower:<BUILD_NUMBER> for traceability
        //   -t ${IMAGE_LATEST} : also tag as iris-flower:latest (floating pointer)
        //   --pull             : always pull the latest base image (python:3.10-slim)
        //                        to pick up OS security patches automatically
        //   ./iris-flower-ci   : build context — the folder containing the Dockerfile
        //                        (relative to WORKSPACE, which is the repo root)
        stage('Build Docker Image') {
            steps {
                echo '─────────────────────────────────────────'
                echo " STAGE 9 — Build Docker image: ${IMAGE_NAME}"
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            echo 'Building Docker image...'
                            docker build \
                                --pull \
                                -t ${IMAGE_NAME} \
                                -t ${IMAGE_LATEST} \
                                ./${PROJECT_DIR}
                            echo 'Image built successfully.'
                            docker images | grep iris-flower
                        """
                    } else {
                        bat """
                            echo Building Docker image...
                            docker build ^
                                --pull ^
                                -t ${IMAGE_NAME} ^
                                -t ${IMAGE_LATEST} ^
                                .\\${PROJECT_DIR}
                            echo Image built successfully.
                            docker images | findstr iris-flower
                        """
                    }
                }
            }
        }

        // ── Stage 10: Deploy Container ────────────────────────────────────────
        // Removes any existing container with the same name (avoids "name
        // already in use" errors on re-runs), then starts a fresh container.
        //
        // `docker rm -f ... || true`
        //   The `|| true` (Unix) / `|| exit 0` (Windows) pattern means:
        //   "if the container doesn't exist yet, that's fine — keep going."
        //   Without it, Jenkins would fail the stage on the very first build
        //   because there is no old container to remove.
        //
        // `docker run` flags:
        //   --name ${CONTAINER_NAME}  : gives the container a fixed, predictable name
        //   --rm                      : auto-delete the container when it exits
        //                               (we archive the model in Stage 8 already)
        //   ${IMAGE_LATEST}           : always run the image we just built
        stage('Deploy Container') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 10 — Remove old container and start new one'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh """
                            echo 'Removing old container if it exists...'
                            docker rm -f ${CONTAINER_NAME} || true

                            echo 'Starting new container...'
                            docker run \
                                --name ${CONTAINER_NAME} \
                                ${IMAGE_LATEST}

                            echo 'Container finished executing.'
                        """
                    } else {
                        bat """
                            echo Removing old container if it exists...
                            docker rm -f ${CONTAINER_NAME} || exit 0

                            echo Starting new container...
                            docker run ^
                                --name ${CONTAINER_NAME} ^
                                ${IMAGE_LATEST}

                            echo Container finished executing.
                        """
                    }
                }
            }
        }

        // ── Stage 11: Container Logs ──────────────────────────────────────────
        // Prints the full stdout/stderr from the completed container into the
        // Jenkins build log. This makes the training results and predictions
        // visible directly in the Jenkins UI without needing to ssh into a host.
        //
        // Note: `docker logs` works on exited containers too — the container
        // does not need to still be running.
        stage('Container Logs') {
            steps {
                echo '─────────────────────────────────────────'
                echo ' STAGE 11 — Print container logs'
                echo '─────────────────────────────────────────'
                script {
                    if (isUnix()) {
                        sh "docker logs ${CONTAINER_NAME}"
                    } else {
                        bat "docker logs ${CONTAINER_NAME}"
                    }
                }
            }
        }
    }

    // =========================================================================
    // POST ACTIONS
    // =========================================================================
    post {

        success {
            echo '============================================'
            echo '  PIPELINE PASSED — image built and run!'
            echo '============================================'
            // mail to: 'team@example.com',
            //      subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "All stages passed. Docker image: ${IMAGE_NAME}\nSee: ${BUILD_URL}"
        }

        failure {
            echo '============================================'
            echo '  PIPELINE FAILED — check the logs above.'
            echo '============================================'
            // mail to: 'team@example.com',
            //      subject: "FAILURE: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "Pipeline failed.\nSee: ${BUILD_URL}"
        }

        changed {
            echo "Build status changed — was: ${currentBuild.previousBuild?.result}"
        }

        always {
            echo "Build result : ${currentBuild.currentResult}"
            echo "Duration     : ${currentBuild.durationString}"

            // Clean up dangling/untagged Docker images to prevent disk exhaustion.
            // `|| true` prevents this housekeeping step from failing the build
            // if there are no dangling images to prune.
            script {
                if (isUnix()) {
                    sh "docker image prune -f || true"
                } else {
                    bat "docker image prune -f || exit 0"
                }
            }
        }
    }
}
