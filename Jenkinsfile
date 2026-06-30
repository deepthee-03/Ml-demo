// =============================================================================
// Jenkinsfile — Declarative Pipeline for Iris Flower ML Project
// =============================================================================
// Repo layout assumed:
//   ML_LAB/                        ← repo root (this file lives here)
//   ├── Jenkinsfile
//   └── iris-flower-ci/
//       ├── train.py
//       ├── predict.py
//       ├── test_model.py
//       └── requirements.txt
// =============================================================================

pipeline {

    // ── Agent ─────────────────────────────────────────────────────────────────
    // 'any' lets Jenkins pick any available node.
    // Replace with agent { label 'linux' } or agent { label 'windows' }
    // to pin to a specific node type.
    agent any

    // ── Global environment variables ──────────────────────────────────────────
    environment {
        PROJECT_DIR  = 'iris-flower-ci'               // subfolder with all source
        VENV_DIR     = "${WORKSPACE}\\${PROJECT_DIR}\\venv"  // virtualenv root
        MODEL_FILE   = 'iris_model.pkl'               // artifact produced by train.py
        REPORTS_DIR  = "${WORKSPACE}\\${PROJECT_DIR}\\reports" // test/lint reports
        MIN_ACCURACY = '0.90'                         // documented threshold (informational)
    }

    // ── Pipeline-wide options ─────────────────────────────────────────────────
    options {
        timestamps()                              // prefix every log line with a timestamp
        timeout(time: 30, unit: 'MINUTES')        // abort runaway builds after 30 min
        buildDiscarder(logRotator(numToKeepStr: '10'))  // keep only the last 10 builds
        disableConcurrentBuilds()                 // prevent overlapping runs on the same branch
    }

    // =========================================================================
    // STAGES
    // =========================================================================
    stages {

        // ── Stage 1: Checkout ─────────────────────────────────────────────────
        // Clones/updates the repository on the Jenkins agent.
        // `checkout scm` uses the SCM configuration from the Jenkins job itself,
        // so no hardcoded URL is needed — the job stays portable.
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
        // Creates an isolated Python virtualenv so dependencies never bleed
        // into the system Python or other Jenkins jobs.
        // Supports both Windows (bat) and Unix (sh) agents via isUnix().
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
        // Upgrades pip first (avoids resolver bugs in older pip versions),
        // then installs all packages listed in requirements.txt.
        // flake8 is added here for the code-quality stage that follows.
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
        // Runs flake8 on all Python files in the project directory.
        // --max-line-length=120  — relaxed limit suitable for ML scripts
        // --statistics           — prints a count of each error code found
        // --exit-zero            — report issues but do NOT fail the build;
        //                          remove this flag to make quality a hard gate.
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
        // Runs all tests in test_model.py.
        // --junitxml writes a JUnit-format XML report so Jenkins can parse it,
        // display a test trend graph, and mark individual test cases as
        // passed/failed/skipped in the UI.
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
                // Publish JUnit results regardless of pass/fail so Jenkins
                // always shows the test trend graph on the job page.
                always {
                    junit "${PROJECT_DIR}/reports/test-results.xml"
                }
            }
        }

        // ── Stage 6: Train ML Model ───────────────────────────────────────────
        // Runs train.py which:
        //   1. Loads the Iris dataset
        //   2. Trains a Logistic Regression classifier
        //   3. Evaluates and prints metrics
        //   4. Writes iris_model.pkl to the project directory
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
        // Confirms that iris_model.pkl was actually written by train.py.
        // A missing model file here means training silently failed — catching
        // this early prevents a confusing "file not found" error downstream.
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
        // Stores the trained model and test reports in Jenkins so they can be
        // downloaded from the build page at any time.
        // fingerprint: true  — Jenkins computes an MD5 hash of each artifact,
        //                       enabling traceability across builds and jobs.
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
    }

    // =========================================================================
    // POST ACTIONS — run after all stages regardless of outcome
    // =========================================================================
    post {

        // Runs only when every stage above passed.
        success {
            echo '============================================'
            echo '  PIPELINE PASSED — model trained & tested!'
            echo '============================================'
            // Uncomment and configure to send an email on success:
            // mail to: 'team@example.com',
            //      subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "All stages passed.\nSee: ${BUILD_URL}"
        }

        // Runs only when at least one stage failed.
        failure {
            echo '============================================'
            echo '  PIPELINE FAILED — check the logs above.'
            echo '============================================'
            // Uncomment and configure to send an email on failure:
            // mail to: 'team@example.com',
            //      subject: "FAILURE: ${JOB_NAME} #${BUILD_NUMBER}",
            //      body: "The pipeline failed at stage: ${FAILED_STAGE}\nSee: ${BUILD_URL}"
        }

        // Runs when the build status changed from the previous build
        // (e.g., fixed after failure, or newly broken).
        changed {
            echo "Build status changed — was: ${currentBuild.previousBuild?.result}"
        }

        // Runs on every build, regardless of outcome. Use for cleanup.
        always {
            echo "Build result : ${currentBuild.currentResult}"
            echo "Duration     : ${currentBuild.durationString}"
            // Clean up the virtualenv to reclaim disk space on the agent.
            // Remove the comment below to enable cleanup after every run:
            // script {
            //     if (isUnix()) { sh "rm -rf ${PROJECT_DIR}/venv" }
            //     else { bat "rd /s /q ${PROJECT_DIR}\\venv" }
            // }
        }
    }
}
