const vm = Vue.createApp({
    data() {
        return {
            searchTerm: '',
            searchResults: null,
            noResults: null,
            errorMessage: null,
            loading: false,
            apiUrl: 'http://localhost:8000/api/',
            fields: {},
        }
    },
    methods: {
        search() {
            if (this.searchTerm === '') {
                return;
            }

            this.loading = true;
            this.searchResults = null;
            this.errorMessage = null;
            this.noResults = null;

            axios.get(this.apiUrl, {params: {search: this.searchTerm}})
                .then(response => {
                    if (Object.keys(response.data).length === 0) {
                        this.noResults = true;
                    } else {
                        this.searchResults = response.data;
                        console.log(this.searchResults)
                        this.fields = parseFields(response.data)
                    }
                    this.loading = false;
                })
                .catch(error => {
                    this.errorMessage = error.message;
                    this.loading = false;
                });


        },
    },
}).mount('#app')


function parseFields(data) {
    const obj = JSON.parse(JSON.stringify(data));
    const result = {};

    for (let key in obj) {
        const items = obj[key];
        if (Array.isArray(items) && items.length > 0) {
            const firstItem = items[0];
            const fields = Object.keys(firstItem);
            result[key] = fields;
        }
    }
    console.log(result)
    return result;
}