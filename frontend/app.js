(function () {
  const form = document.querySelector('#query-form');
  const queryInput = document.querySelector('#query');
  const useDemoCheckbox = document.querySelector('#use-demo');
  const endpointField = document.querySelector('#endpoint');
  const statusEl = document.querySelector('#status');
  const resultsSection = document.querySelector('#results');
  const exportButton = document.querySelector('#export-json');

  const analysisList = document.querySelector('#analysis-list');
  const planList = document.querySelector('#plan-list');
  const explanationList = document.querySelector('#explanation-list');
  const factList = document.querySelector('#fact-check-list');
  const quizList = document.querySelector('#quiz-list');
  const profileList = document.querySelector('#profile-list');

  let latestResult = null;

  function toggleEndpointField() {
    const disabled = useDemoCheckbox.checked;
    endpointField.disabled = disabled;
    endpointField.parentElement.classList.toggle('disabled', disabled);
  }

  function updateStatus(message, type = 'info') {
    statusEl.textContent = message;
    statusEl.dataset.state = type;
    statusEl.classList.remove('hidden');
  }

  function clearStatus() {
    statusEl.textContent = '';
    statusEl.dataset.state = '';
    statusEl.classList.add('hidden');
  }

  function setLoading(isLoading) {
    if (isLoading) {
      updateStatus('Running Lumira tutoring pipeline...');
      form.querySelector('button[type="submit"]').disabled = true;
      exportButton.disabled = true;
    } else {
      form.querySelector('button[type="submit"]').disabled = false;
      exportButton.disabled = !latestResult;
    }
  }

  async function fetchTutoringResult(query, endpoint, useDemo) {
    if (useDemo || !endpoint) {
      return createMockResult(query);
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Request failed (${response.status}): ${text || response.statusText}`);
    }

    return response.json();
  }

  function renderAnalysis(analysis) {
    analysisList.innerHTML = '';
    if (!analysis) {
      analysisList.innerHTML = '<li>No analysis returned.</li>';
      return;
    }

    Object.entries(analysis).forEach(([key, value]) => {
      const li = document.createElement('li');
      const title = document.createElement('div');
      title.className = 'badge';
      title.textContent = key.replace(/_/g, ' ');
      const content = document.createElement('div');
      content.textContent = Array.isArray(value) ? value.join(', ') : String(value);
      li.appendChild(title);
      li.appendChild(content);
      analysisList.appendChild(li);
    });
  }

  function renderPlan(plan) {
    planList.innerHTML = '';
    if (!plan || !plan.length) {
      planList.innerHTML = '<li>No plan steps returned.</li>';
      return;
    }

    plan.forEach((step, index) => {
      const li = document.createElement('li');
      li.className = 'plan-step';
      const stepHeading = document.createElement('h3');
      stepHeading.textContent = `${index + 1}. ${step.title || 'Step'}`;
      const description = document.createElement('p');
      description.textContent = step.description || 'No description provided.';
      li.appendChild(stepHeading);
      li.appendChild(description);
      planList.appendChild(li);
    });
  }

  function renderExplanation(explanation) {
    explanationList.innerHTML = '';
    if (!explanation || !explanation.length) {
      explanationList.innerHTML = '<li>No explanation generated.</li>';
      return;
    }

    explanation.forEach((segment) => {
      const li = document.createElement('li');
      const title = document.createElement('h3');
      title.textContent = segment.step_title || 'Segment';
      const content = document.createElement('p');
      content.textContent = segment.content || '';
      li.appendChild(title);
      li.appendChild(content);

      if (segment.references && segment.references.length) {
        const refs = document.createElement('p');
        refs.className = 'helper-text';
        refs.textContent = `References: ${segment.references.join(', ')}`;
        li.appendChild(refs);
      }

      explanationList.appendChild(li);
    });
  }

  function renderFactCheck(results) {
    factList.innerHTML = '';
    if (!results || !results.length) {
      factList.innerHTML = '<li>No fact-check data available.</li>';
      return;
    }

    results.forEach((result) => {
      const li = document.createElement('li');
      const verdict = document.createElement('span');
      verdict.className = 'badge fact-badge';
      verdict.dataset.verdict = result.verdict || 'uncertain';
      verdict.textContent = (result.verdict || 'unknown').toUpperCase();

      const claim = document.createElement('p');
      claim.textContent = result.claim || 'No claim provided.';

      const confidence = document.createElement('p');
      if (typeof result.confidence === 'number') {
        const percent = Math.round(result.confidence * 100);
        confidence.textContent = `Confidence: ${percent}%`;
      } else {
        confidence.textContent = 'Confidence: n/a';
      }
      confidence.className = 'helper-text';

      li.appendChild(verdict);
      li.appendChild(claim);
      li.appendChild(confidence);
      factList.appendChild(li);
    });
  }

  function renderQuiz(quiz) {
    quizList.innerHTML = '';
    if (!quiz || !quiz.length) {
      quizList.innerHTML = '<li>No formative questions generated.</li>';
      return;
    }

    quiz.forEach((item, index) => {
      const li = document.createElement('li');
      const prompt = document.createElement('h3');
      prompt.textContent = `${index + 1}. ${item.prompt || 'Question'}`;
      const choices = document.createElement('ol');
      choices.start = 1;
      choices.className = 'helper-text';

      (item.choices || []).forEach((choice, choiceIdx) => {
        const choiceItem = document.createElement('li');
        const text = document.createElement('span');
        text.textContent = choice;
        if (choiceIdx === item.answer_index) {
          text.className = 'badge';
          text.textContent = `✔ ${choice}`;
        }
        choiceItem.appendChild(text);
        choices.appendChild(choiceItem);
      });

      li.appendChild(prompt);
      li.appendChild(choices);
      quizList.appendChild(li);
    });
  }

  function renderProfile(profile) {
    profileList.innerHTML = '';
    if (!profile) {
      profileList.innerHTML = '<li>No learner profile returned.</li>';
      return;
    }

    const entries = {
      'Learner ID': profile.learner_id,
      Level: profile.level,
      'Completed Topics': (profile.completed_topics || []).join(', ') || 'None yet',
      Interests: (profile.interests || []).join(', ') || 'None provided',
      Misconceptions: (profile.misconceptions || []).join(', ') || 'None recorded',
    };

    Object.entries(entries).forEach(([label, value]) => {
      const li = document.createElement('li');
      const heading = document.createElement('h3');
      heading.textContent = label;
      const content = document.createElement('p');
      content.textContent = value;
      li.appendChild(heading);
      li.appendChild(content);
      profileList.appendChild(li);
    });
  }

  function renderResults(data) {
    renderAnalysis(data.analysis);
    renderPlan(data.plan);
    renderExplanation(data.explanation);
    renderFactCheck(data.fact_check);
    renderQuiz(data.quiz);
    renderProfile(data.profile);
    resultsSection.classList.remove('hidden');
    latestResult = data;
    exportButton.disabled = false;
    clearStatus();
  }

  function downloadJson() {
    if (!latestResult) return;
    const blob = new Blob([JSON.stringify(latestResult, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    link.href = url;
    link.download = `lumira-tutor-${timestamp}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    const query = queryInput.value.trim();
    const endpoint = endpointField.value.trim();
    const useDemo = useDemoCheckbox.checked;

    if (!query) {
      updateStatus('Please provide a learner question before running the tutor.', 'error');
      return;
    }

    setLoading(true);
    try {
      const data = await fetchTutoringResult(query, endpoint, useDemo);
      renderResults(data);
    } catch (error) {
      console.error(error);
      updateStatus(`Unable to retrieve tutoring data: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  }

  function createMockResult(query) {
    const base = window.SAMPLE_TUTORING_RESPONSE
      ? JSON.parse(JSON.stringify(window.SAMPLE_TUTORING_RESPONSE))
      : {
          analysis: { intent: 'concept', subject: 'general', difficulty: 'unknown' },
          plan: [],
          explanation: [],
          fact_check: [],
          quiz: [],
          profile: {},
        };

    if (query) {
      base.analysis = base.analysis || {};
      base.analysis.query = query;
      if (Array.isArray(base.explanation) && base.explanation.length) {
        base.explanation[0].content = `${base.explanation[0].content}\n\n(Generated for: "${query}")`;
      }
    }

    return new Promise((resolve) => {
      setTimeout(() => resolve(base), 450);
    });
  }

  function bootstrap() {
    useDemoCheckbox.checked = true;
    toggleEndpointField();
    exportButton.disabled = true;
    clearStatus();
    form.addEventListener('submit', handleSubmit);
    useDemoCheckbox.addEventListener('change', toggleEndpointField);
    exportButton.addEventListener('click', downloadJson);
  }

  document.addEventListener('DOMContentLoaded', bootstrap);
})();
