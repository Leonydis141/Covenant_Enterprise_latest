const core = require('@actions/core');
const exec = require('@actions/exec');
const path = require('path');

async function run() {
  try {
    const pythonVersion = core.getInput('python-version');
    const testPath = core.getInput('test-path');
    const coverageThreshold = core.getInput('coverage-threshold');

    // Set up Python
    await exec.exec('python', ['-m', 'pip', 'install', '--upgrade', 'pip']);
    await exec.exec('pip', ['install', 'pytest', 'pytest-cov']);

    // Install backend dependencies
    await exec.exec('pip', ['install', '-r', 'backend/requirements.txt']);

    // Run pytest with coverage
    const exitCode = await exec.exec(
      'pytest',
      [
        testPath,
        '--cov=src/covenant',
        `--cov-fail-under=${coverageThreshold}`,
        '--cov-report=xml:coverage.xml',
        '--cov-report=html',
      ],
      { cwd: 'backend' }
    );

    // Upload coverage reports (you can use actions/upload-artifact later)
    core.setOutput('test-exit-code', exitCode.toString());
  } catch (error) {
    core.setFailed(`Test run failed: ${error.message}`);
  }
}

run();
