document.addEventListener('DOMContentLoaded', function() {
    // --- STATE ---
    let currentCanteen = null;
    let calculationDebounce = null;

    // --- ELEMENTS ---
    const canteenSelect = document.getElementById('canteenSelect');
    const inputs = {
        guests: document.getElementById('guestsInput'),
        days: document.getElementById('daysInput'),
        redMeat: document.getElementById('redMeatSlider'),
        brightMeat: document.getElementById('brightMeatSlider'),
        fish: document.getElementById('fishSlider'),
        organic: document.getElementById('organicSlider'),
        season: document.getElementById('seasonSlider'),
        wastePrep: document.getElementById('wastePrepInput'),
        wasteBuffet: document.getElementById('wasteBuffetInput'),
        wastePlate: document.getElementById('wastePlateInput')
    };
    
    const displays = {
        redMeat: document.getElementById('redMeatVal'),
        brightMeat: document.getElementById('brightMeatVal'),
        fish: document.getElementById('fishVal'),
        veg: document.getElementById('vegVal'),
        organic: document.getElementById('organicVal'),
        season: document.getElementById('seasonVal'),
        totalSavings: document.getElementById('totalSavingsVal'),
        currentImpact: document.getElementById('currentImpactVal'),
        optimizedImpact: document.getElementById('optimizedImpactVal'),
        flights: document.getElementById('flightsVal'),
        trees: document.getElementById('treesVal'),
        recList: document.getElementById('recommendationsList'),
        breakdown: document.getElementById('breakdownBars')
    };

    // --- INITIALIZATION ---
    fetchCanteens();
    setupEventListeners();

    // --- EVENT LISTENERS ---
    function setupEventListeners() {
        canteenSelect.addEventListener('change', loadCanteenData);
        
        // Sliders
        inputs.redMeat.addEventListener('input', () => { updateMeatSliders('red'); calculate(); });
        inputs.brightMeat.addEventListener('input', () => { updateMeatSliders('bright'); calculate(); });
        inputs.fish.addEventListener('input', () => { updateMeatSliders('fish'); calculate(); });
        
        inputs.organic.addEventListener('input', (e) => { 
            displays.organic.textContent = e.target.value + '%'; 
            calculate(); 
        });
        
        inputs.season.addEventListener('input', (e) => { 
            displays.season.textContent = e.target.value + '%'; 
            calculate(); 
        });

        // Inputs
        inputs.guests.addEventListener('change', calculate);
        inputs.days.addEventListener('change', calculate);
        inputs.wastePrep.addEventListener('change', calculate);
        inputs.wasteBuffet.addEventListener('change', calculate);
        inputs.wastePlate.addEventListener('change', calculate);
    }

    // --- DATA FETCHING ---
    async function fetchCanteens() {
        try {
            const response = await fetch('/api/canteens');
            const canteens = await response.json();
            
            canteenSelect.innerHTML = '<option value="">Vælg en kantine...</option>';
            canteens.forEach(c => {
                const option = document.createElement('option');
                option.value = c.id;
                option.textContent = c.name;
                canteenSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching canteens:', error);
        }
    }

    async function loadCanteenData() {
        const id = canteenSelect.value;
        if (!id) return;

        try {
            const response = await fetch(`/api/canteen/${id}`);
            const data = await response.json();
            
            if (data.error) return;

            currentCanteen = data;
            
            // Populate Inputs
            document.getElementById('locationInput').value = data.details.location || '';
            inputs.guests.value = data.details.employees || 0;
            inputs.days.value = data.details.operating_days || 240;

            // Set Sliders (Menu)
            const menu = data.details.menu_composition;
            inputs.redMeat.value = menu.red_meat_percent;
            inputs.brightMeat.value = menu.bright_meat_percent;
            inputs.fish.value = menu.fish_percent;
            
            updateMeatSliders(null); // Update text displays

            // Set Sustainability
            inputs.organic.value = Math.round(data.details.organic_profile.total_percent);
            displays.organic.textContent = inputs.organic.value + '%';
            
            inputs.season.value = Math.round(data.details.sourcing.seasonal_percent);
            displays.season.textContent = inputs.season.value + '%';

            // Set Waste
            inputs.wastePrep.value = data.waste.breakdown.preparation;
            inputs.wasteBuffet.value = data.waste.breakdown.buffet;
            inputs.wastePlate.value = data.waste.breakdown.plate;

            // Initial Calculation
            calculate();

        } catch (error) {
            console.error('Error loading canteen details:', error);
        }
    }

    // --- LOGIC ---
    function updateMeatSliders(changedSource) {
        let red = parseFloat(inputs.redMeat.value);
        let bright = parseFloat(inputs.brightMeat.value);
        let fish = parseFloat(inputs.fish.value);
        
        // Ensure total doesn't exceed 100
        const total = red + bright + fish;
        
        if (total > 100) {
            // Simple normalization logic: reduce others proportionally
            // This is a bit complex to do perfectly UX-wise, so for now we just clamp the current one
            // or let the user mess up and show negative veg (which we clamp to 0 visualy)
            // Better approach: Clamp the changed input so it fits
            
            if (changedSource === 'red') {
                red = 100 - bright - fish;
                inputs.redMeat.value = red;
            } else if (changedSource === 'bright') {
                bright = 100 - red - fish;
                inputs.brightMeat.value = bright;
            } else if (changedSource === 'fish') {
                fish = 100 - red - bright;
                inputs.fish.value = fish;
            }
        }

        const veg = Math.max(0, 100 - red - bright - fish);

        displays.redMeat.textContent = red + '%';
        displays.brightMeat.textContent = bright + '%';
        displays.fish.textContent = fish + '%';
        displays.veg.textContent = veg.toFixed(1) + '%';
    }

    function calculate() {
        if (calculationDebounce) clearTimeout(calculationDebounce);
        calculationDebounce = setTimeout(performCalculation, 300);
    }

    async function performCalculation() {
        if (!currentCanteen) return;

        const payload = {
            employees: parseInt(inputs.guests.value),
            meals_per_day: 1.0, // Assumption
            operating_days: parseInt(inputs.days.value),
            attendance_rate: 0.85, // Assumption
            meat_distribution: {
                red_meat_percent: parseFloat(inputs.redMeat.value),
                bright_meat_percent: parseFloat(inputs.brightMeat.value),
                fish_percent: parseFloat(inputs.fish.value),
                vegetarian_percent: parseFloat(displays.veg.textContent)
            },
            organic_percent: {
                meat: parseFloat(inputs.organic.value), // Simplified: applying total org % to all categories
                vegetables: parseFloat(inputs.organic.value),
                dairy: parseFloat(inputs.organic.value)
            },
            waste: {
                preparation: parseFloat(inputs.wastePrep.value),
                plate: parseFloat(inputs.wastePlate.value),
                buffet: parseFloat(inputs.wasteBuffet.value)
            },
            portion_sizes: {
                protein_gram: 120,
                vegetables_gram: 200,
                carbs_gram: 150
            },
            local_sourcing: 50, // Default
            seasonal_produce: parseFloat(inputs.season.value)
        };

        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const result = await response.json();
            if (result.error) throw new Error(result.error);

            updateUI(result);

        } catch (error) {
            console.error('Calculation error:', error);
        }
    }

    function updateUI(result) {
        // 1. Savings
        // We need a baseline to calculate savings. 
        // Ideally the backend returns "baseline" vs "current scenario".
        // For now, let's assume the "Current Impact" is the FIRST calculation we did, 
        // or we fetch the static baseline from DB.
        // Simplified: We show the calculated Annual Tons as "Optimized Impact"
        // and we need a "Current Impact" to compare against.
        // Let's use the currentCanteen's static CO2/kg * meals * days as baseline estimate.
        
        const baselineCo2PerKg = currentCanteen.details.current_co2_per_kg;
        const totalMeals = parseInt(inputs.guests.value) * parseInt(inputs.days.value) * 0.85; // 0.85 attendance
        const baselineTons = (baselineCo2PerKg * 0.5 * totalMeals) / 1000; // 0.5kg meal size assumption

        const optimizedTons = result.annual_tons;
        const savings = Math.max(0, baselineTons - optimizedTons);

        displays.totalSavings.textContent = savings.toFixed(1);
        displays.currentImpact.textContent = baselineTons.toFixed(1);
        displays.optimizedImpact.textContent = optimizedTons.toFixed(1);

        // 2. Analogies
        // 1 ton CO2 = ~2 London flights (approx 500kg each)
        // 1 ton CO2 = ~50 trees planted (absorb ~20kg/year)
        displays.flights.textContent = Math.round(savings * 2);
        displays.trees.textContent = Math.round(savings * 50);

        // 3. Recommendations
        displays.recList.innerHTML = '';
        result.recommendations.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'p-4 hover:bg-stone-50 transition-colors';
            div.innerHTML = `
                <div class="flex justify-between items-start mb-1">
                    <h4 class="font-bold text-stone-800 text-sm">${rec.title}</h4>
                    <span class="text-xs font-bold text-cb-green-dark bg-cb-green-light/20 px-2 py-1 rounded">
                        -${rec.annual_saving_tons.toFixed(1)} tons
                    </span>
                </div>
                <p class="text-xs text-stone-500">${rec.description}</p>
            `;
            displays.recList.appendChild(div);
        });

        // 4. Breakdown Bars
        displays.breakdown.innerHTML = '';
        const categories = [
            { key: 'red_meat', label: 'Rødt Kød', color: 'bg-cb-red-medium' },
            { key: 'bright_meat', label: 'Lyst Kød', color: 'bg-cb-yellow-medium' },
            { key: 'fish', label: 'Fisk', color: 'bg-cb-blue-medium' },
            { key: 'vegetarian', label: 'Grønt', color: 'bg-cb-green-medium' },
            { key: 'waste', label: 'Madspild', color: 'bg-stone-400' }
        ];

        const maxVal = Math.max(...Object.values(result.breakdown));
        
        categories.forEach(cat => {
            const val = result.breakdown[cat.key];
            const pct = (val / result.per_meal_kg) * 100; // % of total
            
            const bar = document.createElement('div');
            bar.className = 'flex items-center gap-3 text-xs';
            bar.innerHTML = `
                <div class="w-20 font-bold text-stone-600">${cat.label}</div>
                <div class="flex-1 bg-stone-100 rounded-full h-3 overflow-hidden">
                    <div class="${cat.color} h-full rounded-full" style="width: ${pct}%"></div>
                </div>
                <div class="w-12 text-right text-stone-500">${val.toFixed(2)} kg</div>
            `;
            displays.breakdown.appendChild(bar);
        });
    }

    // --- SCENARIOS ---
    window.applyScenario = function(type) {
        if (type === 'meat_free_day') {
            // Reduce meat by ~20% (1/5 days)
            inputs.redMeat.value = inputs.redMeat.value * 0.8;
            inputs.brightMeat.value = inputs.brightMeat.value * 0.8;
            updateMeatSliders(null);
        } else if (type === 'less_beef') {
            inputs.redMeat.value = inputs.redMeat.value * 0.5;
            updateMeatSliders(null);
        } else if (type === 'seasonal_boost') {
            inputs.season.value = 80;
            displays.season.textContent = '80%';
        } else if (type === 'zero_waste') {
            inputs.wastePrep.value = 2;
            inputs.wasteBuffet.value = 2;
            inputs.wastePlate.value = 2;
        }
        calculate();
    };
});
