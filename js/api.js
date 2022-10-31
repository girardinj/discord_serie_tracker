
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
 }

 function warn(s, time_ms=3000) {
    let warning_thing = document.getElementById('warning-container')
    warning_thing.innerHTML = s
    sleep(time_ms).then(_ => {
        warning_thing.innerHTML = ''
    })
 }

function init() {
    let c = document.getElementById('debug-container')
    c.innerHTML = 'loading...'

    if (typeof pywebview === 'undefined') {
        sleep(500).then(init)
        return
    }

    pywebview.api.init_html().then(response => {
        loadChannels(_ => {
            c.innerHTML = 'loaded!'
            API_READY = true
        })
    })
}

function loadChannels(end_function) {
    pywebview.api.load_channels().then(response => {
        let container = document.getElementById('response-container-list')

        response.channels.forEach(channel => {
            let option = document.createElement('option')
            option.value = channel.id
            option.innerHTML = channel.name
            container.appendChild(option)
        })

        end_function()
    })
}

function increment_episode() {
    increment(true)
}

function increment_season() {
    increment(false)
}

function increment(increment_episode) {
    if (API_READY) {
        let channels_list_selector = document.getElementById('response-container-list')
        let selected_id = channels_list_selector.value

        document.getElementById('debug-container').innerHTML = selected_id
        pywebview.api.increment(selected_id, increment_episode).then(_ => {
            warn('incremented ! (maybe wait a bit to see it change)')
        })
    } else {
        warn('client is not ready yet, please wait a bit')
    }
}

function create_new_channel() {
    if (API_READY) {
        let name = document.getElementById('new_channel_input').value.trim()
        
        if (name.trim() === '') {
            warn('please put a name')
        }
        else {
            pywebview.api.create_text_channel(name)
            warn('created ! (maybe wait a bit to see it change)<br>reload to see it in the list')
        }
    } else {
        warn('client is not ready yet, please wait a bit')
    }
}

let API_READY = false
