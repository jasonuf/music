
const curr_title = document.getElementById('curr_title');
const curr_details = document.getElementById('curr_details');
const curr_state = document.querySelector('.card_status');
const imageElement = document.querySelector(".card__image img");
const black_image = imageElement.src;

const POLL_INTERVAL = 30_000;
let endTimer = null;

const fillEl = document.querySelector('.card__progress-fill');


let playbackState = {
  position_ms: 0,
  duration_ms: 1,
  is_playing: false,
  lastFetchedAt: Date.now(),
};

let songState = {
  title: null,
  artist: null,
  album: null,
  album_release: null,
  album_picture: null,

  new_song: false
}

async function fetchPlaybackState() {
  try {

    const response = await fetch('/api/data');
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }


    const data = await response.json();

    console.log(data);

    const { title, artist, position, album, album_release, album_picture, song_length, playing} = data;

    const isNewSong = title !== songState.title || artist !== songState.artist;

    playbackState = {
      position_ms: position,
      duration_ms: song_length,
      is_playing: playing,
      lastFetchedAt: Date.now(),
    };

    songState = {
      title: title,
      artist: artist,
      album: album,
      album_release: album_release,
      album_picture: album_picture,

      new_song:  isNewSong
    };

    updateBar();

    if (endTimer) clearTimeout(endTimer);
    if (playbackState.is_playing) {
      const elapsed = Date.now() - playbackState.lastFetchedAt;
      const currentPos = playbackState.position_ms + elapsed;
      const remainingMs = playbackState.duration_ms - currentPos;
      if (remainingMs > 0) {
        endTimer = setTimeout(fetchPlaybackState, remainingMs + 1500);
      }
    } else {

      endTimer = null;
    }


    if (songState.new_song){
      updateSong();
      updateRecentlyPlayed(songState);
      updateCounts(songState);
      songState.new_song = false;
    }

    if (!title){
      curr_state.textContent = `Paused`;
    }
    else if (!playbackState.is_playing){
      curr_state.textContent = `Paused`;
    }
    else{
      curr_state.textContent = `Playing`;
    }

  } catch (error) {
    console.error("Could not fetch data:", error);
    curr_title.textContent = 'Failed to load user data.';
    curr_details.textContent = ``;
    imageElement.src = black_image;
  }
}

function updateRecentlyPlayed({ title, artist, album_picture }) {
  const container = document.getElementById('recently_played');
  const heading   = container.querySelector('h3');
  const newRow    = document.createElement('div');
  newRow.className = 'data-card__row';
  newRow.innerHTML = `
    <div class="data-card__image">
      <img src="${album_picture}" alt="Album art">
    </div>
    <div class="data-card__info">${title} - ${artist}</div>
  `;
  heading.insertAdjacentElement('afterend', newRow);


  const rows = container.querySelectorAll('.data-card__row');
  if (rows.length > 6) rows[rows.length - 1].remove();
}

function updateCounts({ artist, title, album }) {
  // Generic sorter/helper
  function bumpAndReorder(containerSelector, matchFn, parseFn) {
    const container = document.querySelector(containerSelector);
    const rows = Array.from(container.querySelectorAll('.data-card__row'));

    rows.forEach(row => {
      const info = row.querySelector('.data-card__info');
      let { key, count } = parseFn(info.textContent);

      if (matchFn(key)) {
        count++;
        info.textContent = `${key}: ${count}`;
      }

      // stash for sorting
      row._count = count;
    });

    // sort descending by the updated count
    rows.sort((a, b) => b._count - a._count);

    // re-attach in new order
    rows.forEach(r => container.appendChild(r));
  }

  // Top Artists: key = artist name
  bumpAndReorder(
    '#top_artist',
    key => key === artist,
    text => {
      const [name, cnt] = text.split(':').map(s => s.trim());
      return { key: name, count: Number(cnt) };
    }
  );

  // Top Songs: key = "Title - Artist"
  bumpAndReorder(
    '#top_songs',
    key => key === `${title} - ${artist}`,
    text => {
      const idx = text.lastIndexOf(':');
      const key = text.slice(0, idx).trim();
      const cnt = Number(text.slice(idx + 1).trim());
      return { key, count: cnt };
    }
  );

  // Top Albums: key = album name
  bumpAndReorder(
    '#top_albums',
    key => key === album,
    text => {
      const [name, cnt] = text.split(':').map(s => s.trim());
      return { key: name, count: Number(cnt) };
    }
  );
}

function updateSong() {
  if (songState.title === null){
      curr_title.textContent = `No Song Playing`;
      curr_details.textContent = ``;
      imageElement.src = black_image;
  }
  else{
    curr_title.textContent = `${songState.title}`;
    curr_details.textContent = `${songState.artist} • ${songState.album} • ${songState.album_release}`;
    imageElement.src = songState.album_picture;
  }
}


function updateBar() {

  const elapsed = Date.now() - playbackState.lastFetchedAt;

  const currentPos = playbackState.is_playing
    ? playbackState.position_ms + elapsed
    : playbackState.position_ms;

  const clampedPos = Math.min(currentPos, playbackState.duration_ms);

  const pct = (clampedPos / playbackState.duration_ms) * 100;
  fillEl.style.width = pct + '%';
}


function animationLoop() {
  updateBar();
  requestAnimationFrame(animationLoop);
}

fetchPlaybackState();
setInterval(fetchPlaybackState, POLL_INTERVAL);
requestAnimationFrame(animationLoop);