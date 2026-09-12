(function () {
  "use strict";

  var root = document.getElementById("unknown-scoreboard-root");
  if (!root) return;

  var CATEGORY_ORDER = ["Web", "Pwn", "Reversing", "Crypto", "OSINT", "Misc"];
  var CATEGORY_LABEL = {
    Web: "WEB",
    Pwn: "PWN",
    Reversing: "REV",
    Crypto: "CRYPTO",
    OSINT: "OSINT",
    Misc: "MISC",
  };
  var CATEGORY_CLASS = {
    Web: "cat-web",
    Pwn: "cat-pwn",
    Reversing: "cat-reversing",
    Crypto: "cat-crypto",
    OSINT: "cat-osint",
    Misc: "cat-misc",
  };

  var state = {
    standings: [],
    challenges: [],
    solvesByChallenge: {},
    accountSolves: {},
    accountSolveCount: {},
    view: "overview",
    currentUserId: window.init ? window.init.userId : null,
  };

  var els = {
    loading: document.getElementById("sb-loading"),
    empty: document.getElementById("sb-empty"),
    overviewPanel: document.getElementById("sb-overview"),
    detailedPanel: document.getElementById("sb-detailed"),
    overviewBody: document.getElementById("sb-overview-body"),
    podium: document.getElementById("sb-podium"),
    tableWrap: document.getElementById("sb-table-wrap"),
    matrixWrap: document.getElementById("sb-matrix-wrap"),
    matrixHead: document.getElementById("sb-matrix-head"),
    matrixBody: document.getElementById("sb-matrix-body"),
    statTeams: document.getElementById("sb-stat-teams"),
    statChallenges: document.getElementById("sb-stat-challenges"),
    statSolves: document.getElementById("sb-stat-solves"),
    updated: document.getElementById("sb-updated"),
    toggleBtns: Array.prototype.slice.call(
      root.querySelectorAll(".unknown-sb-toggle-btn"),
    ),
  };

  var modal = document.getElementById("sb-team-modal");
  var modalBody = document.getElementById("sb-team-modal-body");

  function escapeHtml(str) {
    return String(str == null ? "" : str).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function accentVar(category) {
    var map = {
      Web: "--unk-web",
      Pwn: "--unk-pwn",
      Reversing: "--unk-reversing",
      Crypto: "--unk-crypto",
      OSINT: "--unk-osint",
      Misc: "--unk-misc",
    };
    return "var(" + (map[category] || "--unk-muted") + ")";
  }

  function formatTime(iso) {
    if (!iso) return "";
    try {
      return new Date(iso).toLocaleString();
    } catch (e) {
      return iso;
    }
  }

  async function fetchJson(url) {
    try {
      var res = await fetch(url, {
        credentials: "same-origin",
        headers: { Accept: "application/json" },
      });
      if (!res.ok) return null;
      var body = await res.json();
      return body && body.success ? body.data : null;
    } catch (e) {
      return null;
    }
  }

  async function loadData() {
    var standings = (await fetchJson("/api/v1/scoreboard")) || [];
    var challenges = (await fetchJson("/api/v1/challenges")) || [];

    challenges = challenges.slice().sort(function (a, b) {
      return (
        Number(a.value || 0) - Number(b.value || 0) ||
        String(a.name).localeCompare(String(b.name))
      );
    });

    var solvesByChallenge = {};
    await Promise.all(
      challenges.map(async function (c) {
        var solves = await fetchJson("/api/v1/challenges/" + c.id + "/solves");
        solvesByChallenge[c.id] = solves || [];
      }),
    );

    var accountSolves = {};
    var accountSolveCount = {};
    Object.keys(solvesByChallenge).forEach(function (chalId) {
      solvesByChallenge[chalId].forEach(function (solve, idx) {
        var accId = solve.account_id;
        if (!accountSolves[accId]) accountSolves[accId] = {};
        accountSolves[accId][chalId] = { date: solve.date, firstBlood: idx === 0 };
        accountSolveCount[accId] = (accountSolveCount[accId] || 0) + 1;
      });
    });

    state.standings = standings;
    state.challenges = challenges;
    state.solvesByChallenge = solvesByChallenge;
    state.accountSolves = accountSolves;
    state.accountSolveCount = accountSolveCount;
  }

  function totalSolves() {
    var total = 0;
    Object.keys(state.solvesByChallenge).forEach(function (id) {
      total += state.solvesByChallenge[id].length;
    });
    return total;
  }

  function getCategories() {
    var present = [];
    state.challenges.forEach(function (c) {
      if (present.indexOf(c.category) === -1) present.push(c.category);
    });
    return CATEGORY_ORDER.filter(function (cat) {
      return present.indexOf(cat) !== -1;
    });
  }

  function rankRowClass(rank) {
    if (rank === 1) return "sb-rank-gold";
    if (rank === 2) return "sb-rank-silver";
    if (rank === 3) return "sb-rank-bronze";
    return "";
  }

  function isCurrentUser(accountId) {
    return (
      state.currentUserId != null &&
      String(state.currentUserId) === String(accountId)
    );
  }

  function renderStats() {
    els.statTeams.textContent = state.standings.length;
    els.statChallenges.textContent = state.challenges.length;
    els.statSolves.textContent = totalSolves();
  }

  function renderPodium() {
    var top3 = state.standings.slice(0, 3);
    if (top3.length < 3) {
      els.podium.innerHTML = "";
      els.podium.hidden = true;
      return;
    }
    els.podium.hidden = false;
    els.podium.innerHTML = top3
      .map(function (s, i) {
        var rank = i + 1;
        var me = isCurrentUser(s.account_id);
        return (
          '<a class="unknown-sb-podium-card sb-rank-' +
          rank +
          (me ? " is-current-user" : "") +
          '" href="' +
          escapeHtml(s.account_url) +
          '">' +
          '<span class="unknown-sb-podium-rank">#' + rank + "</span>" +
          "<strong>" + escapeHtml(s.name) + "</strong>" +
          '<span class="unknown-sb-podium-score"><b>' +
          s.score +
          "</b> PTS</span>" +
          (me ? "<small>YOU</small>" : "") +
          "</a>"
        );
      })
      .join("");
  }

  function renderOverview() {
    renderPodium();
    els.overviewBody.innerHTML = state.standings
      .map(function (s, i) {
        var rank = i + 1;
        var me = isCurrentUser(s.account_id);
        var solves = state.accountSolveCount[s.account_id] || 0;
        return (
          '<tr class="' +
          rankRowClass(rank) +
          (me ? " is-current-user" : "") +
          '">' +
          '<td class="sb-col-rank"><span class="unknown-sb-rank-pill">' +
          rank +
          "</span></td>" +
          '<td class="sb-col-team"><button type="button" class="sb-team-link" data-team-id="' +
          escapeHtml(s.account_id) +
          '">' +
          escapeHtml(s.name) +
          "</button>" +
          (me ? '<span class="unknown-sb-you">YOU</span>' : "") +
          "</td>" +
          '<td class="sb-col-score"><strong>' + s.score + "</strong></td>" +
          '<td class="sb-col-solves">' +
          (state.accountSolveCount[s.account_id] || 0) +
          "</td>" +
          "</tr>"
        );
      })
      .join("");
  }

  function renderMatrix() {
    var categories = getCategories();
    var byCategory = {};
    categories.forEach(function (cat) {
      byCategory[cat] = [];
    });
    state.challenges.forEach(function (c) {
      if (byCategory[c.category]) byCategory[c.category].push(c);
    });

    var headRow1 = [
      '<tr><th class="sb-matrix-team-col sb-matrix-corner" rowspan="2">Team</th>',
    ];
    categories.forEach(function (cat) {
      headRow1.push(
        '<th class="sb-matrix-cat-head ' +
        CATEGORY_CLASS[cat] +
        '" style="--accent:' +
        accentVar(cat) +
        '" colspan="' +
        byCategory[cat].length +
        '">' +
        CATEGORY_LABEL[cat] +
        "</th>",
      );
    });
    headRow1.push('<th class="sb-matrix-total-col" rowspan="2">Score</th></tr>');

    var headRow2 = ["<tr>"];
    var orderedChallenges = [];
    categories.forEach(function (cat) {
      byCategory[cat].forEach(function (c) {
        orderedChallenges.push(c);
        var title = c.name + " · " + c.value + "pts · " + cat;
        headRow2.push(
          '<th class="sb-matrix-chal-head ' +
          CATEGORY_CLASS[cat] +
          '" title="' +
          escapeHtml(title) +
          '"><span>' +
          escapeHtml(c.name) +
          "</span></th>",
        );
      });
    });
    headRow2.push("</tr>");

    els.matrixHead.innerHTML = headRow1.join("") + headRow2.join("");

    els.matrixBody.innerHTML = state.standings
      .map(function (s, i) {
        var rank = i + 1;
        var me = isCurrentUser(s.account_id);
        var solveMap = state.accountSolves[s.account_id] || {};
        var cells = orderedChallenges
          .map(function (c) {
            var solve = solveMap[c.id];
            if (!solve) {
              return '<td class="sb-matrix-cell ' + CATEGORY_CLASS[c.category] + '"></td>';
            }
            if (solve.firstBlood) {
              return (
                '<td class="sb-matrix-cell is-first-blood ' +
                CATEGORY_CLASS[c.category] +
                '" title="First Blood · ' +
                escapeHtml(c.name) +
                '"><i class="fas fa-gem"></i></td>'
              );
            }
            return (
              '<td class="sb-matrix-cell is-solved ' +
              CATEGORY_CLASS[c.category] +
              '" title="Solved · ' +
              escapeHtml(c.name) +
              '"><i class="fas fa-check"></i></td>'
            );
          })
          .join("");

        return (
          '<tr class="' +
          rankRowClass(rank) +
          (me ? " is-current-user" : "") +
          '">' +
          '<td class="sb-matrix-team-col"><button type="button" class="sb-team-link" data-team-id="' +
          escapeHtml(s.account_id) +
          '"><span class="unknown-sb-rank-pill sm">' +
          rank +
          "</span>" +
          escapeHtml(s.name) +
          "</button></td>" +
          cells +
          '<td class="sb-matrix-total-col">' + s.score + "</td>" +
          "</tr>"
        );
      })
      .join("");
  }

  function openTeamModal(accountId) {
    var idx = state.standings.findIndex(function (s) {
      return String(s.account_id) === String(accountId);
    });
    if (idx === -1) return;

    var s = state.standings[idx];
    var rank = idx + 1;
    var solveMap = state.accountSolves[s.account_id] || {};
    var solvedCount = Object.keys(solveMap).length;

    var rows = state.challenges
      .map(function (c) {
        var solve = solveMap[c.id];
        var statusClass = solve
          ? solve.firstBlood
            ? "is-first-blood"
            : "is-solved"
          : "is-unsolved";
        var statusText = solve
          ? solve.firstBlood
            ? "First Blood"
            : "Solved"
          : "Unsolved";
        var statusIcon = solve
          ? solve.firstBlood
            ? '<i class="fas fa-gem"></i>'
            : '<i class="fas fa-check"></i>'
          : "";
        return (
          '<div class="sb-tm-row ' + statusClass + '">' +
          '<span class="sb-tm-cat" style="--accent:' + accentVar(c.category) + '"></span>' +
          '<span class="sb-tm-name">' + escapeHtml(c.name) + " (" + c.value + "pts)</span>" +
          '<span class="sb-tm-time">' + (solve ? escapeHtml(formatTime(solve.date)) : "") + "</span>" +
          '<span class="sb-tm-status">' + statusIcon + statusText + "</span>" +
          "</div>"
        );
      })
      .join("");

    modalBody.innerHTML =
      '<div class="sb-tm-head">' +
      "<div>" +
      '<span class="sb-tm-rank">Rank #' + rank + "</span>" +
      "<h2>" + escapeHtml(s.name) + "</h2>" +
      "</div>" +
      "</div>" +
      '<div class="sb-tm-stats">' +
      '<div class="sb-tm-stat"><strong>' + s.score + "</strong><span>Score</span></div>" +
      '<div class="sb-tm-stat"><strong>' + solvedCount + "</strong><span>Solved</span></div>" +
      '<div class="sb-tm-stat"><strong>#' + rank + "</strong><span>Rank</span></div>" +
      "</div>" +
      '<div class="sb-tm-section">' +
      "<span>Challenges</span>" +
      '<div class="sb-tm-list">' + rows + "</div>" +
      "</div>" +
      '<a class="sb-tm-profile-link" href="' +
      escapeHtml(s.account_url) +
      '">View Full Profile &rarr;</a>';

    modal.hidden = false;
    document.body.classList.add("unknown-sb-modal-open");
  }

  function closeTeamModal() {
    modal.hidden = true;
    document.body.classList.remove("unknown-sb-modal-open");
  }

  function currentViewFromUrl() {
    var params = new URLSearchParams(window.location.search);
    return params.get("view") === "detailed" ? "detailed" : "overview";
  }

  function setView(view, pushState) {
    state.view = view;
    els.overviewPanel.hidden = view !== "overview";
    els.detailedPanel.hidden = view !== "detailed";
    els.toggleBtns.forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.view === view);
    });

    if (pushState) {
      var url = new URL(window.location.href);
      if (view === "detailed") {
        url.searchParams.set("view", "detailed");
      } else {
        url.searchParams.delete("view");
      }
      var qs = url.searchParams.toString();
      history.replaceState(null, "", url.pathname + (qs ? "?" + qs : "") + url.hash);
    }
  }

  async function refresh() {
    await loadData();
    renderStats();
    renderOverview();
    renderMatrix();

    var hasData = state.standings.length > 0;
    els.empty.hidden = hasData;
    els.tableWrap.hidden = !hasData;
    els.matrixWrap.hidden = !hasData;
    els.updated.textContent = hasData
      ? "Updated " + new Date().toLocaleTimeString()
      : "";
  }

  els.toggleBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setView(btn.dataset.view, true);
    });
  });

  root.addEventListener("click", function (e) {
    var link = e.target.closest(".sb-team-link");
    if (link) {
      openTeamModal(link.dataset.teamId);
    }
  });

  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target.closest("[data-modal-close]")) closeTeamModal();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !modal.hidden) closeTeamModal();
    });
  }

  window.addEventListener("popstate", function () {
    setView(currentViewFromUrl(), false);
  });

  (async function init() {
    await refresh();
    els.loading.hidden = true;
    setView(currentViewFromUrl(), false);

    var interval = window.scoreboardUpdateInterval || 300000;
    setInterval(refresh, interval);
  })();
})();
