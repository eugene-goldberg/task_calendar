// Calendar state
let currentDate = new Date();
let selectedDate = null;
let events = {};

// Load events from localStorage
function loadEvents() {
    const savedEvents = localStorage.getItem('calendarEvents');
    if (savedEvents) {
        events = JSON.parse(savedEvents);
    }
}

// Save events to localStorage
function saveEvents() {
    localStorage.setItem('calendarEvents', JSON.stringify(events));
}

// Initialize calendar
function init() {
    loadEvents();
    renderCalendar();
    setupEventListeners();
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('prev-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById('next-month').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    // Modal controls
    const modal = document.getElementById('event-modal');
    const closeBtn = document.querySelector('.close');
    
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    document.getElementById('save-event').addEventListener('click', saveEvent);
    document.getElementById('delete-event').addEventListener('click', deleteEvent);
}

// Render calendar
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Update header
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December'];
    document.getElementById('current-month').textContent = `${monthNames[month]} ${year}`;
    
    // Clear calendar days
    const calendarDays = document.getElementById('calendar-days');
    calendarDays.innerHTML = '';
    
    // Get first day of month and number of days
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    
    // Add blank cells for days before the first day of month
    for (let i = 0; i < firstDay; i++) {
        const blankElement = createBlankDayElement();
        calendarDays.appendChild(blankElement);
    }
    
    // Add current month's days
    const today = new Date();
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const dayElement = createDayElement(date, false);
        
        // Check if it's today
        if (date.toDateString() === today.toDateString()) {
            dayElement.classList.add('today');
        }
        
        calendarDays.appendChild(dayElement);
    }
    
    // Add blank cells to complete the grid
    const totalCells = calendarDays.children.length;
    const remainingCells = 42 - totalCells; // 6 weeks * 7 days
    for (let i = 0; i < remainingCells; i++) {
        const blankElement = createBlankDayElement();
        calendarDays.appendChild(blankElement);
    }
}

// Create blank day element
function createBlankDayElement() {
    const blankElement = document.createElement('div');
    blankElement.className = 'calendar-day blank';
    return blankElement;
}

// Create day element
function createDayElement(date, isOtherMonth) {
    const dayElement = document.createElement('div');
    dayElement.className = 'calendar-day';
    if (isOtherMonth) {
        dayElement.classList.add('other-month');
    }
    
    // Add day number
    const dayNumber = document.createElement('div');
    dayNumber.className = 'day-number';
    dayNumber.textContent = date.getDate();
    dayElement.appendChild(dayNumber);
    
    // Add events
    const dateKey = formatDateKey(date);
    console.log(`Checking events for ${dateKey}:`, events[dateKey]);
    if (events[dateKey]) {
        events[dateKey].forEach(event => {
            const eventElement = createEventElement(event);
            dayElement.appendChild(eventElement);
            // Adjust font size after element is in DOM
            requestAnimationFrame(() => {
                adjustEventFontSize(eventElement);
            });
        });
    }
    
    // Add click handler
    dayElement.addEventListener('click', (e) => {
        if (!e.target.classList.contains('event')) {
            openEventModal(date);
        }
    });
    
    return dayElement;
}

// Create event element
function createEventElement(event) {
    const eventElement = document.createElement('div');
    eventElement.className = 'event default';
    eventElement.textContent = event.title;
    eventElement.dataset.eventId = event.id;
    
    eventElement.addEventListener('click', (e) => {
        e.stopPropagation();
        openEventModal(new Date(event.date), event);
    });
    
    return eventElement;
}

// Adjust font size to fit text
function adjustEventFontSize(element) {
    if (!element.parentElement) return;
    
    const cellWidth = element.parentElement.offsetWidth;
    const cellHeight = element.parentElement.offsetHeight;
    const padding = 12; // Total horizontal padding
    const availableWidth = cellWidth * 0.95 - padding;
    const minSize = 8;
    const maxSize = 24;
    
    // Get text content
    const text = element.textContent;
    const words = text.split(' ').length;
    
    // Remove debug logging
    
    // Calculate font size based on content length and cell size
    let fontSize = 12;
    
    // For calendar cells, we want readable text that can wrap
    // Prioritize readability over fitting on one line
    if (words <= 3) {
        // Very short text (1-3 words) - scale up significantly
        fontSize = 16;
    } else if (words <= 6) {
        // Medium text (4-6 words) - moderate size
        fontSize = 14;
    } else {
        // Longer text - keep at base size or smaller
        fontSize = 12;
        
        // Check if even at 12px it needs to be smaller
        element.style.fontSize = '12px';
        element.style.whiteSpace = 'normal';
        
        // If the element is too tall, scale down
        if (element.offsetHeight > cellHeight * 0.8) {
            fontSize = 10;
        }
    }
    
    // Apply font size within bounds
    fontSize = Math.min(Math.max(fontSize, minSize), maxSize);
    element.style.fontSize = fontSize + 'px';
    
    // Ensure text doesn't overflow vertically
    if (element.offsetHeight > cellHeight * 0.9) {
        fontSize = Math.max(fontSize - 2, minSize);
        element.style.fontSize = fontSize + 'px';
    }
}

// Open event modal
function openEventModal(date, event = null) {
    selectedDate = date;
    const modal = document.getElementById('event-modal');
    const titleInput = document.getElementById('event-title');
    const deleteBtn = document.getElementById('delete-event');
    
    if (event) {
        titleInput.value = event.title;
        deleteBtn.style.display = 'inline-block';
        deleteBtn.dataset.eventId = event.id;
    } else {
        titleInput.value = '';
        deleteBtn.style.display = 'none';
    }
    
    modal.style.display = 'block';
    titleInput.focus();
}

// Save event
function saveEvent() {
    const title = document.getElementById('event-title').value.trim();
    if (!title) return;
    
    if (!selectedDate) {
        console.error('No date selected');
        return;
    }
    
    const dateKey = formatDateKey(selectedDate);
    console.log('Saving event - dateKey:', dateKey, 'title:', title);
    
    if (!events[dateKey]) {
        events[dateKey] = [];
        console.log('Created new array for date:', dateKey);
    }
    
    const deleteBtn = document.getElementById('delete-event');
    const eventId = deleteBtn.dataset.eventId;
    console.log('Event ID from delete button:', eventId);
    
    if (eventId) {
        // Update existing event
        const eventIndex = events[dateKey].findIndex(e => e.id === eventId);
        if (eventIndex !== -1) {
            events[dateKey][eventIndex] = {
                id: eventId,
                title,
                date: selectedDate.toISOString()
            };
            console.log('Updated existing event at index:', eventIndex);
        }
    } else {
        // Create new event
        const newEvent = {
            id: Date.now().toString(),
            title,
            date: selectedDate.toISOString()
        };
        events[dateKey].push(newEvent);
        console.log('Created new event:', newEvent);
        console.log('Events array after push:', events[dateKey]);
    }
    
    saveEvents();
    console.log('Event saved:', {dateKey, title});
    console.log('Current events:', events);
    console.log('About to render calendar for:', currentDate.toISOString());
    renderCalendar();
    document.getElementById('event-modal').style.display = 'none';
}

// Delete event
function deleteEvent() {
    const eventId = this.dataset.eventId;
    const dateKey = formatDateKey(selectedDate);
    
    if (events[dateKey]) {
        events[dateKey] = events[dateKey].filter(e => e.id !== eventId);
        if (events[dateKey].length === 0) {
            delete events[dateKey];
        }
    }
    
    saveEvents();
    renderCalendar();
    document.getElementById('event-modal').style.display = 'none';
}

// Format date key for storage
function formatDateKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}