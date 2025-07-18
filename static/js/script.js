// Calendar state
let currentDate = new Date();
let selectedDate = null;
let events = {};

// API base URL
const API_BASE_URL = '/api';

// Get access token from localStorage
function getAccessToken() {
    return localStorage.getItem('access_token');
}

// Add authentication header to requests
function getAuthHeaders() {
    const token = getAccessToken();
    if (!token) {
        window.location.href = '/login';
        return {};
    }
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
}

// Load events from API
async function loadEvents() {
    try {
        const response = await fetch(`${API_BASE_URL}/events`, {
            headers: getAuthHeaders()
        });
        if (response.ok) {
            events = await response.json();
        } else if (response.status === 401) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Save event via API
async function saveEvent(dateKey, eventData) {
    try {
        const response = await fetch(`${API_BASE_URL}/events/${dateKey}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(eventData)
        });
        if (response.ok) {
            return await response.json();
        } else if (response.status === 401) {
            window.location.href = '/login';
        }
        return null;
    } catch (error) {
        console.error('Error saving event:', error);
        return null;
    }
}

// Update event via API
async function updateEvent(dateKey, eventId, eventData) {
    try {
        const response = await fetch(`${API_BASE_URL}/events/${dateKey}/${eventId}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify({ title: eventData.title })
        });
        if (response.status === 401) {
            window.location.href = '/login';
            return false;
        }
        return response.ok;
    } catch (error) {
        console.error('Error updating event:', error);
        return false;
    }
}

// Delete event via API
async function deleteEventAPI(dateKey, eventId, deleteAll = false) {
    try {
        const url = `${API_BASE_URL}/events/${dateKey}/${eventId}${deleteAll ? '?delete_all=true' : ''}`;
        const response = await fetch(url, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        if (response.status === 401) {
            window.location.href = '/login';
            return false;
        }
        return response.ok;
    } catch (error) {
        console.error('Error deleting event:', error);
        return false;
    }
}

// Initialize calendar
async function init() {
    await loadEvents();
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
    
    // Close modal when clicking outside
    document.getElementById('event-modal').addEventListener('click', (e) => {
        if (e.target.id === 'event-modal') {
            e.target.style.display = 'none';
        }
    });
    
    // Close modal when clicking the X button
    document.querySelector('.close').addEventListener('click', () => {
        document.getElementById('event-modal').style.display = 'none';
    });
    
    // Save event
    document.getElementById('save-event').addEventListener('click', saveEventHandler);
    
    // Delete event
    document.getElementById('delete-event').addEventListener('click', deleteEvent);
    
    // Logout
    document.getElementById('logout-btn').addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
    });
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
    
    // Add blank cells for days before the first day of month
    for (let i = 0; i < firstDay; i++) {
        const blankDay = document.createElement('div');
        blankDay.className = 'calendar-day other-month';
        // Leave the cell empty - no date number
        calendarDays.appendChild(blankDay);
    }
    
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const dayElement = createDayElement(date);
        calendarDays.appendChild(dayElement);
    }
    
    // Add blank cells to complete the last row only
    const totalCells = calendarDays.children.length;
    const lastRowCells = totalCells % 7;
    
    if (lastRowCells !== 0) {
        const remainingCells = 7 - lastRowCells;
        for (let i = 0; i < remainingCells; i++) {
            const blankDay = document.createElement('div');
            blankDay.className = 'calendar-day other-month';
            // Leave the cell empty - no date number
            calendarDays.appendChild(blankDay);
        }
    }
}

// Create day element
function createDayElement(date) {
    const dayElement = document.createElement('div');
    dayElement.className = 'calendar-day';
    
    // Highlight today
    const today = new Date();
    if (date.toDateString() === today.toDateString()) {
        dayElement.classList.add('today');
    }
    
    // Add day number
    const dayNumber = document.createElement('div');
    dayNumber.className = 'day-number';
    dayNumber.textContent = date.getDate();
    dayElement.appendChild(dayNumber);
    
    // Add events
    const dateKey = formatDateKey(date);
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
        console.log('Day clicked:', date, 'Target:', e.target);
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
    console.log('Opening modal for date:', date);
    selectedDate = date;
    const modal = document.getElementById('event-modal');
    const titleInput = document.getElementById('event-title');
    const deleteBtn = document.getElementById('delete-event');
    
    if (!modal) {
        console.error('Modal element not found!');
        return;
    }
    
    // Update modal title
    document.getElementById('modal-date').textContent = date.toDateString();
    
    // Reset checkboxes
    document.getElementById('recur-daily').checked = false;
    document.getElementById('recur-weekly').checked = false;
    document.getElementById('recur-monthly').checked = false;
    document.getElementById('recur-quarterly').checked = false;
    
    if (event) {
        // Edit existing event
        titleInput.value = event.title;
        deleteBtn.style.display = 'block';
        deleteBtn.dataset.eventId = event.id;
        
        // Hide recurrence options for existing events
        document.querySelector('.recurrence-options').style.display = 'none';
    } else {
        // New event
        titleInput.value = '';
        deleteBtn.style.display = 'none';
        deleteBtn.dataset.eventId = '';
        
        // Show recurrence options for new events
        document.querySelector('.recurrence-options').style.display = 'block';
    }
    
    modal.style.display = 'flex';
    titleInput.focus();
}

// Save event handler
async function saveEventHandler() {
    const title = document.getElementById('event-title').value.trim();
    if (!title) {
        alert('Please enter an event title');
        return;
    }
    
    if (!selectedDate) {
        console.error('No date selected');
        return;
    }
    
    const dateKey = formatDateKey(selectedDate);
    
    if (!events[dateKey]) {
        events[dateKey] = [];
    }
    
    const deleteBtn = document.getElementById('delete-event');
    const eventId = deleteBtn.dataset.eventId;
    
    let success = false;
    
    if (eventId) {
        // Update existing event
        success = await updateEvent(dateKey, eventId, { title });
        if (success) {
            const eventIndex = events[dateKey].findIndex(e => e.id === eventId);
            if (eventIndex !== -1) {
                events[dateKey][eventIndex].title = title;
            }
        }
    } else {
        // Get selected recurrence options
        const recurrenceTypes = [];
        if (document.getElementById('recur-daily').checked) {
            recurrenceTypes.push('daily');
        }
        if (document.getElementById('recur-weekly').checked) {
            recurrenceTypes.push('weekly');
        }
        if (document.getElementById('recur-monthly').checked) {
            recurrenceTypes.push('monthly');
        }
        if (document.getElementById('recur-quarterly').checked) {
            recurrenceTypes.push('quarterly');
        }
        
        // Create new event
        const newEvent = {
            id: Date.now().toString(),
            title,
            date: selectedDate.toISOString(),
            recurrence_types: recurrenceTypes
        };
        
        const response = await saveEvent(dateKey, newEvent);
        if (response) {
            // Reload all events to show recurring events
            await loadEvents();
            success = true;
        }
    }
    
    if (success) {
        renderCalendar();
        document.getElementById('event-modal').style.display = 'none';
    } else {
        alert('Failed to save event. Please try again.');
    }
}

// Delete event
async function deleteEvent() {
    const eventId = this.dataset.eventId;
    const dateKey = formatDateKey(selectedDate);
    
    // Check if event is part of a recurring series
    const event = events[dateKey]?.find(e => e.id === eventId);
    let deleteAll = false;
    
    if (event && event.recurrence_group_id) {
        const choice = confirm('This is a recurring event. Delete all occurrences?\n\nOK = Delete all\nCancel = Delete only this event');
        deleteAll = choice;
    } else {
        if (!confirm('Are you sure you want to delete this event?')) {
            return;
        }
    }
    
    const success = await deleteEventAPI(dateKey, eventId, deleteAll);
    
    if (success) {
        // Reload all events to reflect changes
        await loadEvents();
        renderCalendar();
        document.getElementById('event-modal').style.display = 'none';
    } else {
        alert('Failed to delete event. Please try again.');
    }
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