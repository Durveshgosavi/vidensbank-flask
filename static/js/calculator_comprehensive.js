document.addEventListener('DOMContentLoaded', function() {
    // --- VERIFIED DANISH DATA (CONCITO & Our World in Data 2024) ---
    const CO2_FACTORS = {
        // kg CO2e per kg of food (Source: Poore & Nemecek 2018, CONCITO)
        beef: 60.0,          // Oksekød
        lamb: 24.0,          // Lammekød
        pork: 12.0,          // Svinekød
        chicken: 6.9,        // Kylling
        fish: 6.0,           // Fisk (gennemsnit)
        eggs: 4.8,           // Æg
        dairy: 3.2,          // Mejeriprodukter
        legumes: 2.0,        // Bælgfrugter
        vegetables: 2.0,     // Grøntsager
        grains: 1.4,         // Korn
        fruits: 1.1          // Frugt
    };

    // Protein sources mapped to CO2 factors
    const PROTEIN_CO2 = {
        red_meat: (CO2_FACTORS.beef + CO2_FACTORS.lamb) / 2,  // Average: 42 kg
        bright_meat: (CO2_FACTORS.pork + CO2_FACTORS.chicken) / 2,  // Average: 9.45 kg
        fish: CO2_FACTORS.fish,  // 6 kg
        vegetarian: CO2_FACTORS.legumes  // 2 kg
    };

    // Waste impact multiplier
    const WASTE_MULTIPLIER = {
        low: 1.05,      // <5% total waste
        medium: 1.15,   // 5-15% total waste
        high: 1.30      // >15% total waste
    };

    // Seasonal/local reduction factors
    const SEASONAL_BENEFIT = 0.15;  // 15% reduction for fully seasonal
    const LOCAL_BENEFIT = 0.10;     // 10% reduction for fully local

    // Cost estimates (DKK)
    const CO2_COST_PER_TON = 1800;  // Danish carbon tax estimate

    // --- STATE ---
    let currentCanteen = null;
    let calculationDebounce = null;
    let baselineImpact = null;

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
            canteenSelect.innerHTML = '<option value="">Fejl ved indlæsning...</option>';
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
            inputs.guests.value = data.details.employees || 150;
            inputs.days.value = data.details.operating_days || 240;

            // Set Sliders (Menu)
            const menu = data.details.menu_composition;
            inputs.redMeat.value = menu.red_meat_percent;
            inputs.brightMeat.value = menu.bright_meat_percent;
            inputs.fish.value = menu.fish_percent;

            updateMeatSliders(null);

            // Set Sustainability
            inputs.organic.value = Math.round(data.details.organic_profile.total_percent);
            displays.organic.textContent = inputs.organic.value + '%';

            inputs.season.value = Math.round(data.details.sourcing.seasonal_percent);
            displays.season.textContent = inputs.season.value + '%';

            // Set Waste
            inputs.wastePrep.value = data.waste.breakdown.preparation;
            inputs.wasteBuffet.value = data.waste.breakdown.buffet;
            inputs.wastePlate.value = data.waste.breakdown.plate;

            // Calculate baseline
            baselineImpact = calculateLocalImpact();

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
            if (changedSource === 'red') {
                red = 100 - bright - fish;
                inputs.redMeat.value = Math.max(0, red);
            } else if (changedSource === 'bright') {
                bright = 100 - red - fish;
                inputs.brightMeat.value = Math.max(0, bright);
            } else if (changedSource === 'fish') {
                fish = 100 - red - bright;
                inputs.fish.value = Math.max(0, fish);
            }
        }

        const veg = Math.max(0, 100 - parseFloat(inputs.redMeat.value) - parseFloat(inputs.brightMeat.value) - parseFloat(inputs.fish.value));

        displays.redMeat.textContent = parseFloat(inputs.redMeat.value).toFixed(0) + '%';
        displays.brightMeat.textContent = parseFloat(inputs.brightMeat.value).toFixed(0) + '%';
        displays.fish.textContent = parseFloat(inputs.fish.value).toFixed(0) + '%';
        displays.veg.textContent = veg.toFixed(0) + '%';
    }

    function calculate() {
        if (calculationDebounce) clearTimeout(calculationDebounce);
        calculationDebounce = setTimeout(performCalculation, 300);
    }

    function performCalculation() {
        const result = calculateLocalImpact();
        if (!result) return;

        // If we have a baseline, calculate savings
        if (baselineImpact) {
            const savings = Math.max(0, baselineImpact.annual_tons - result.annual_tons);
            updateUI(result, baselineImpact.annual_tons, savings);
        } else {
            updateUI(result, result.annual_tons, 0);
        }
    }

    function calculateLocalImpact() {
        // Get input values
        const guests = parseInt(inputs.guests.value) || 0;
        const days = parseInt(inputs.days.value) || 240;
        const redMeat = parseFloat(inputs.redMeat.value) / 100;
        const brightMeat = parseFloat(inputs.brightMeat.value) / 100;
        const fish = parseFloat(inputs.fish.value) / 100;
        const veg = 1 - redMeat - brightMeat - fish;

        const seasonalPercent = parseFloat(inputs.season.value) / 100;

        const wastePrep = parseFloat(inputs.wastePrep.value) || 0;
        const wasteBuffet = parseFloat(inputs.wasteBuffet.value) || 0;
        const wastePlate = parseFloat(inputs.wastePlate.value) || 0;
        const totalWaste = wastePrep + wasteBuffet + wastePlate;

        // Calculate meals per year
        const attendanceRate = 0.85;  // 85% attendance assumption
        const annualMeals = guests * days * attendanceRate;

        // Average protein portion weight (kg per meal)
        const proteinPortionKg = 0.120;  // 120g protein per meal

        // Calculate CO2 per protein portion
        const co2PerProtein = (
            redMeat * PROTEIN_CO2.red_meat * proteinPortionKg +
            brightMeat * PROTEIN_CO2.bright_meat * proteinPortionKg +
            fish * PROTEIN_CO2.fish * proteinPortionKg +
            veg * PROTEIN_CO2.vegetarian * proteinPortionKg
        );

        // Add vegetables, grains, dairy (approximate per meal)
        const vegetablesKg = 0.200;  // 200g vegetables
        const grainsKg = 0.150;      // 150g grains/carbs
        const dairyKg = 0.050;       // 50g dairy products

        const co2PerMeal = co2PerProtein +
                          (vegetablesKg * CO2_FACTORS.vegetables) +
                          (grainsKg * CO2_FACTORS.grains) +
                          (dairyKg * CO2_FACTORS.dairy);

        // Apply seasonal/local reductions
        const seasonalReduction = 1 - (seasonalPercent * SEASONAL_BENEFIT);
        const adjustedCo2PerMeal = co2PerMeal * seasonalReduction;

        // Apply waste multiplier
        let wasteMultiplier = 1.0;
        if (totalWaste < 5) wasteMultiplier = WASTE_MULTIPLIER.low;
        else if (totalWaste <= 15) wasteMultiplier = WASTE_MULTIPLIER.medium;
        else wasteMultiplier = WASTE_MULTIPLIER.high;

        const finalCo2PerMeal = adjustedCo2PerMeal * wasteMultiplier;

        // Calculate annual impact
        const annualTons = (finalCo2PerMeal * annualMeals) / 1000;

        // Breakdown by category
        const breakdown = {
            red_meat: redMeat * PROTEIN_CO2.red_meat * proteinPortionKg * wasteMultiplier,
            bright_meat: brightMeat * PROTEIN_CO2.bright_meat * proteinPortionKg * wasteMultiplier,
            fish: fish * PROTEIN_CO2.fish * proteinPortionKg * wasteMultiplier,
            vegetarian: veg * PROTEIN_CO2.vegetarian * proteinPortionKg * wasteMultiplier,
            waste: finalCo2PerMeal * (wasteMultiplier - 1)  // Impact of waste
        };

        // Generate recommendations
        const recommendations = generateRecommendations(
            { redMeat, brightMeat, fish, veg },
            totalWaste,
            seasonalPercent,
            annualMeals,
            finalCo2PerMeal
        );

        return {
            per_meal_kg: finalCo2PerMeal,
            annual_tons: annualTons,
            breakdown: breakdown,
            recommendations: recommendations,
            annual_meals: annualMeals
        };
    }

    function generateRecommendations(meatDist, wastePercent, seasonalPercent, meals, co2PerMeal) {
        const recs = [];

        // Recommendation 1: Reduce red meat
        if (meatDist.redMeat > 0.15) {
            const savingPerMeal = (meatDist.redMeat * 0.5 * PROTEIN_CO2.red_meat * 0.120);
            const annualSaving = (savingPerMeal * meals) / 1000;
            recs.push({
                priority: 1,
                title: "Reducér Rødt Kød med 50%",
                description: `I har ${(meatDist.redMeat * 100).toFixed(0)}% rødt kød. En halvering kan spare betydeligt på klimaaftrykket. Erstat med plantebaserede alternativer eller lyst kød.`,
                annual_saving_tons: annualSaving,
                implementation_time: "3-6 måneder",
                difficulty: "Middel"
            });
        }

        // Recommendation 2: Increase vegetarian
        if (meatDist.veg < 0.30) {
            const increase = 0.30 - meatDist.veg;
            const savingPerMeal = increase * ((PROTEIN_CO2.red_meat * meatDist.redMeat + PROTEIN_CO2.bright_meat * meatDist.brightMeat) / (meatDist.redMeat + meatDist.brightMeat) - PROTEIN_CO2.vegetarian) * 0.120;
            const annualSaving = (savingPerMeal * meals) / 1000;
            recs.push({
                priority: 2,
                title: "Øg Vegetariske Retter til 30%",
                description: `Kun ${(meatDist.veg * 100).toFixed(0)}% vegetarisk nu. Målet om 30% kan reducere emissioner markant. Fokusér på appetitvækkende plantebaserede retter.`,
                annual_saving_tons: annualSaving,
                implementation_time: "1-3 måneder",
                difficulty: "Let"
            });
        }

        // Recommendation 3: Reduce waste
        if (wastePercent > 10) {
            const reduction = wastePercent - 5;  // Target 5%
            const savingPerMeal = co2PerMeal * (reduction / 100);
            const annualSaving = (savingPerMeal * meals) / 1000;
            recs.push({
                priority: 3,
                title: "Minimer Madspild til Under 5%",
                description: `Med ${wastePercent.toFixed(0)}% samlet spild er der betydeligt forbedringspotentiale. Fokusér på bedre portionskontrol og spildregistrering.`,
                annual_saving_tons: annualSaving,
                implementation_time: "2-4 måneder",
                difficulty: "Middel"
            });
        }

        // Recommendation 4: Increase seasonal
        if (seasonalPercent < 0.70) {
            const increase = 0.70 - seasonalPercent;
            const savingPerMeal = co2PerMeal * increase * SEASONAL_BENEFIT;
            const annualSaving = (savingPerMeal * meals) / 1000;
            recs.push({
                priority: 4,
                title: "Brug 70% Sæsonvarer",
                description: `Sæsonvarer reducerer transport-emissioner. Med ${(seasonalPercent * 100).toFixed(0)}% nu, kan I øge til 70% gennem bedre indkøbsplanlægning.`,
                annual_saving_tons: annualSaving,
                implementation_time: "1-2 måneder",
                difficulty: "Let"
            });
        }

        // Sort by annual saving (descending)
        return recs.sort((a, b) => b.annual_saving_tons - a.annual_saving_tons).slice(0, 5);
    }

    function updateUI(result, baselineTons, savings) {
        // 1. Savings
        displays.totalSavings.textContent = savings.toFixed(1);
        displays.currentImpact.textContent = baselineTons.toFixed(1);
        displays.optimizedImpact.textContent = result.annual_tons.toFixed(1);

        // 2. Analogies (verified estimates)
        // 1 ton CO2 ≈ 2.2 flights Copenhagen-London return (0.45 tons each)
        // 1 ton CO2 ≈ 50 trees planted (absorbing 20kg CO2/year for 1 year)
        displays.flights.textContent = Math.round(savings * 2.2);
        displays.trees.textContent = Math.round(savings * 50);

        // 3. Recommendations
        displays.recList.innerHTML = '';
        if (result.recommendations.length === 0) {
            displays.recList.innerHTML = '<div class="p-6 text-center text-stone-500 italic">Godt arbejde! I har allerede optimeret godt. Fortsæt det gode arbejde.</div>';
        } else {
            result.recommendations.forEach((rec, index) => {
                const div = document.createElement('div');
                div.className = 'p-4 hover:bg-stone-50 transition-colors';
                div.innerHTML = `
                    <div class="flex justify-between items-start mb-2">
                        <div class="flex-1">
                            <div class="flex items-center gap-2 mb-1">
                                <span class="inline-block w-6 h-6 rounded-full bg-cb-blue-dark text-white text-xs font-bold flex items-center justify-center">${index + 1}</span>
                                <h4 class="font-bold text-stone-800 text-sm">${rec.title}</h4>
                            </div>
                            <p class="text-xs text-stone-600 leading-relaxed">${rec.description}</p>
                        </div>
                        <span class="ml-3 text-xs font-bold text-cb-green-dark bg-cb-green-light/30 px-3 py-1 rounded whitespace-nowrap">
                            -${rec.annual_saving_tons.toFixed(1)}t
                        </span>
                    </div>
                    <div class="flex gap-3 mt-2 text-xs text-stone-500">
                        <span>⏱ ${rec.implementation_time}</span>
                        <span>•</span>
                        <span>📊 ${rec.difficulty}</span>
                        <span>•</span>
                        <span>💰 ${Math.round(rec.annual_saving_tons * CO2_COST_PER_TON).toLocaleString()} DKK/år</span>
                    </div>
                `;
                displays.recList.appendChild(div);
            });
        }

        // 4. Breakdown Bars
        displays.breakdown.innerHTML = '';
        const categories = [
            { key: 'red_meat', label: 'Rødt Kød', color: 'bg-red-500' },
            { key: 'bright_meat', label: 'Lyst Kød', color: 'bg-orange-500' },
            { key: 'fish', label: 'Fisk', color: 'bg-blue-500' },
            { key: 'vegetarian', label: 'Plantebaseret', color: 'bg-green-500' },
            { key: 'waste', label: 'Madspild', color: 'bg-stone-500' }
        ];

        categories.forEach(cat => {
            const val = result.breakdown[cat.key] || 0;
            const pct = result.per_meal_kg > 0 ? (val / result.per_meal_kg) * 100 : 0;

            const bar = document.createElement('div');
            bar.className = 'flex items-center gap-3 text-sm';
            bar.innerHTML = `
                <div class="w-24 font-bold text-stone-700">${cat.label}</div>
                <div class="flex-1 bg-stone-100 rounded-full h-4 overflow-hidden">
                    <div class="${cat.color} h-full rounded-full transition-all duration-500" style="width: ${pct.toFixed(1)}%"></div>
                </div>
                <div class="w-20 text-right text-stone-600 font-mono">${val.toFixed(2)} kg</div>
                <div class="w-12 text-right text-stone-500 text-xs">${pct.toFixed(0)}%</div>
            `;
            displays.breakdown.appendChild(bar);
        });

        // Add total row
        const totalBar = document.createElement('div');
        totalBar.className = 'flex items-center gap-3 text-sm font-bold pt-3 border-t border-stone-200 mt-2';
        totalBar.innerHTML = `
            <div class="w-24 text-stone-900">Total</div>
            <div class="flex-1"></div>
            <div class="w-20 text-right text-stone-900 font-mono">${result.per_meal_kg.toFixed(2)} kg</div>
            <div class="w-12 text-right text-stone-700 text-xs">100%</div>
        `;
        displays.breakdown.appendChild(totalBar);
    }

    // --- SCENARIOS ---
    window.applyScenario = function(type) {
        if (type === 'meat_free_day') {
            // One meat-free day per week (reduce meat by 20%)
            inputs.redMeat.value = Math.round(inputs.redMeat.value * 0.8);
            inputs.brightMeat.value = Math.round(inputs.brightMeat.value * 0.8);
            updateMeatSliders(null);
        } else if (type === 'less_beef') {
            // Halve red meat consumption
            inputs.redMeat.value = Math.round(inputs.redMeat.value * 0.5);
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
