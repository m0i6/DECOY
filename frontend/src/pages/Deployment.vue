<script setup lang="ts">
import WorldMap from '../components/WorldMap.vue'

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { BACKEND_ROOT_URL } from "../config"

const name = ref<String>('')
const serverType = ref<String>('ssh server')
const description = ref<String>('')
const geolocation = ref<String>('')
const behaviours = ref<String[]>([])
const newBehaviour = ref<String>('')
const creationResult = ref<String>('')

function addBehaviour() {
    if (newBehaviour.value.trim()) {
        behaviours.value.push(newBehaviour.value.trim())
        newBehaviour.value = ''
    }
}

function updateGeolocation(newLocation: string) {
    console.log("setting location in parent thing ", newLocation)
    geolocation.value = newLocation
}

const router = useRouter()

function createHoneypot() {
    setTimeout(() => { creationResult.value = '' }, 5000) // Clear message after 5 seconds
    if (!name.value.trim()) {
        creationResult.value = 'Name is required.'
        return
    }
    if (!serverType.value.trim()) {
        creationResult.value = 'Server type is required.'
        return
    }
    if (behaviours.value.length === 0) {
        creationResult.value = 'At least one behaviour is required.'
        return
    }
    if (!geolocation.value.trim()) {
        creationResult.value = 'Geolocation is required.'
        return
    }
    if (!description.value.trim()) {
        creationResult.value = 'Description is required.'
        return
    }
    // Logik zum Erstellen des Honeypots
    fetch(BACKEND_ROOT_URL + '/HoneyPots/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: name.value,
            behaviours: behaviours.value.join(','),
            server_category: serverType.value,
            geolocation: geolocation.value,
            description: description.value
        })
    }).then(response => {
        if (response.ok) {
            creationResult.value = 'Honeypot created successfully!'
            // redirect to home page
            router.push({ path: '/' })
        } else {
            creationResult.value = 'Failed to create honeypot.'
        }
    }).catch(error => {
        console.error('Error creating honeypot:', error)
        creationResult.value = 'Error occurred while creating honeypot.'
    })
}


</script>

<template>
    <div class="h-full w-full flex items-center justify-center text-white flex-col">
        <div class="border-2 border-slate-600 p-10 rounded-lg ">
            <div class="flex flex-row gap-10">
                <div>
                    <h1 class="text-2xl font-bold">Create new honeypot</h1>
                    <label for="name" class="mt-4 block text-sm font-medium text-slate-300 min-w-[25vw]">Name</label>
                    <input type="text" id="name" v-model="name"
                        class="mt-1 block w-full border border-slate-600 bg-transparent p-2 rounded-lg" />
                    <div class="mt-4">
                        <label for="serverType" class="block text-sm font-medium text-slate-300">Server Type</label>
                        <select id="serverType" v-model="serverType"
                            class="mt-1 block w-full border border-slate-600 bg-transparent p-3 rounded-lg">
                            <option value="" disabled>Select server category</option>
                            <option value="web">Web server honeypot</option>
                            <option value="database">Database honeypot</option>
                            <option value="sftp">SFTP honeypot</option>
                            <option value="other">Other honeypot</option>
                        </select>
                    </div>
                    <div class="mt-4">
                        <label for="behaviours" class="block text-sm font-medium text-slate-300">Behaviour of the
                            honeypot</label>
                        <div class="mt-1 flex flex-col gap-2">
                            <label class="flex items-center">
                                <input type="checkbox" value="SSH Port open" v-model="behaviours" />
                                <span class="ml-2">SSH Port open</span>
                            </label>
                            <label class="flex items-center">
                                <input type="checkbox" value="SQL Injectable server" v-model="behaviours" />
                                <span class="ml-2">SQL Injectable server</span>
                            </label>
                            <label class="flex items-center">
                                <input type="checkbox" value="Weak sftp password" v-model="behaviours" />
                                <span class="ml-2">Weak sftp password</span>
                            </label>
                        </div>
                    </div>
                    <div class="mt-4">
                        <label class="block text-sm font-medium text-slate-300 mb-2">Behaviours</label>
                        <div class="my-2">
                            <span v-for="(behaviour, index) in behaviours" :key="index"
                                class="bg-slate-700 mx-1 px-2 py-1 my-3 rounded">{{ behaviour }}</span>
                        </div>
                        <div class="flex gap-2 mt-4">
                            <input v-model="newBehaviour" type="text" placeholder="New behaviour"
                                class="border border-slate-600 bg-transparent p-2 rounded-lg flex-1" />
                            <button type="button" @click="addBehaviour"
                                class="bg-yellow-200 text-black rounded-lg px-4 py-2">Add</button>
                        </div>
                    </div>
                    <div class="mt-4">
                        <label for="description" class="block text-sm font-medium text-slate-300">Description</label>
                        <input type="text" id="description" v-model="description"
                            placeholder="Enter honeypot description"
                            class="mt-1 block w-full border border-slate-600 bg-transparent p-2 rounded-lg" />
                    </div>
                    <button type="submit" @click="createHoneypot"
                        class="bg-yellow-100 rounded-xl p-2 px-10 my-5 text-black">Create</button>
                </div>
                <WorldMap widthClass="h-full w-full min-w-[300px]" :hasDynamicInput="true"
                    @update-geolocation="updateGeolocation" />
            </div>
            <div v-if="creationResult" class="mt-4 text-red-400 font-semibold">
                {{ creationResult }}
            </div>
        </div>
    </div>
</template>
