/**
 * CLIMATE CALCULATOR ENGINE
 * Shared calculation logic with verified Danish CO2 data
 * Sources: CONCITO Danish Climate Database v2.0, Poore & Nemecek (2018), Our World in Data 2024
 */

// --- VERIFIED DANISH CO2 DATA ---
const CO2_FACTORS = {
    // kg CO2e per kg of food
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
    red_meat: (CO2_FACTORS.beef + CO2_FACTORS.lamb) / 2,      // Average: 42 kg
    bright_meat: (CO2_FACTORS.pork + CO2_FACTORS.chicken) / 2, // Average: 9.45 kg
    fish: CO2_FACTORS.fish,                                     // 6 kg
    vegetarian: CO2_FACTORS.legumes                             // 2 kg
};

// Constants
const WASTE_MULTIPLIER = {
    low: 1.05,      // <5% total waste
    medium: 1.15,   // 5-15% total waste
    high: 1.30      // >15% total waste
};

const SEASONAL_BENEFIT = 0.15;  // 15% reduction for fully seasonal
const CO2_COST_PER_TON_DKK = 1800;  // Danish carbon tax estimate

// Standard portion sizes (kg)
const PORTION_SIZES = {
    protein: 0.120,      // 120g
    vegetables: 0.200,   // 200g
    grains: 0.150,       // 150g
    dairy: 0.050         // 50g
};

/**
 * Calculate climate impact for a canteen
 * @param {Object} params - Calculation parameters
 * @returns {Object} - Calculation results
 */
function calculateCanteenImpact(params) {
    const {
        employees = 150,
        attendance_rate = 0.85,
        operating_days = 240,
        meat_distribution = {
            red_meat_percent: 30,
            bright_meat_percent: 40,
            fish_percent: 15,
            vegetarian_percent: 15
        },
        waste = {
            preparation: 8,
            buffet: 5,
            plate: 12
        },
        seasonal_produce = 50,
        organic_percent = {
            meat: 40,
            vegetables: 60
        }
    } = params;

    // Normalize percentages to decimals
    const redMeat = meat_distribution.red_meat_percent / 100;
    const brightMeat = meat_distribution.bright_meat_percent / 100;
    const fish = meat_distribution.fish_percent / 100;
    const vegetarian = meat_distribution.vegetarian_percent / 100;
    const seasonal = seasonal_produce / 100;

    // Calculate annual meals
    const annualMeals = employees * operating_days * attendance_rate;

    // Calculate CO2 per protein portion
    const co2PerProtein = (
        redMeat * PROTEIN_CO2.red_meat * PORTION_SIZES.protein +
        brightMeat * PROTEIN_CO2.bright_meat * PORTION_SIZES.protein +
        fish * PROTEIN_CO2.fish * PORTION_SIZES.protein +
        vegetarian * PROTEIN_CO2.vegetarian * PORTION_SIZES.protein
    );

    // Add vegetables, grains, dairy
    const co2PerMeal = co2PerProtein +
                      (PORTION_SIZES.vegetables * CO2_FACTORS.vegetables) +
                      (PORTION_SIZES.grains * CO2_FACTORS.grains) +
                      (PORTION_SIZES.dairy * CO2_FACTORS.dairy);

    // Calculate waste multiplier
    const totalWaste = waste.preparation + waste.buffet + waste.plate;
    let wasteMultiplier;
    if (totalWaste < 5) {
        wasteMultiplier = WASTE_MULTIPLIER.low;
    } else if (totalWaste <= 15) {
        wasteMultiplier = WASTE_MULTIPLIER.medium;
    } else {
        wasteMultiplier = WASTE_MULTIPLIER.high;
    }

    // Apply seasonal reduction and waste
    const seasonalReduction = 1 - (seasonal * SEASONAL_BENEFIT);
    const finalCo2PerMeal = co2PerMeal * seasonalReduction * wasteMultiplier;

    // Annual totals
    const annualTons = (finalCo2PerMeal * annualMeals) / 1000;
    const costSavingsDKK = calculateCostSavings(meat_distribution, annualMeals);

    // Breakdown
    const breakdown = {
        protein: {
            red_meat: redMeat * PROTEIN_CO2.red_meat * PORTION_SIZES.protein,
            bright_meat: brightMeat * PROTEIN_CO2.bright_meat * PORTION_SIZES.protein,
            fish: fish * PROTEIN_CO2.fish * PORTION_SIZES.protein,
            vegetarian: vegetarian * PROTEIN_CO2.vegetarian * PORTION_SIZES.protein
        },
        sides: {
            vegetables: PORTION_SIZES.vegetables * CO2_FACTORS.vegetables,
            grains: PORTION_SIZES.grains * CO2_FACTORS.grains,
            dairy: PORTION_SIZES.dairy * CO2_FACTORS.dairy
        },
        waste_impact: co2PerMeal * (wasteMultiplier - 1),
        seasonal_benefit: co2PerMeal * seasonal * SEASONAL_BENEFIT
    };

    // Recommendations
    const recommendations = generateRecommendations(
        meat_distribution,
        totalWaste,
        seasonal_produce,
        annualMeals,
        finalCo2PerMeal
    );

    return {
        success: true,
        results: {
            per_meal_kg: finalCo2PerMeal,
            annual_tons: annualTons,
            annual_meals: annualMeals,
            estimated_cost_savings_dkk: costSavingsDKK,
            breakdown: breakdown,
            recommendations: recommendations,
            analogies: {
                flights_to_london: Math.round(annualTons / 0.25),  // ~250kg per flight
                trees_planted: Math.round(annualTons * 50)         // ~20kg CO2/year per tree
            }
        }
    };
}

/**
 * Calculate potential cost savings from reduced emissions
 */
function calculateCostSavings(meatDist, annualMeals) {
    // Calculate potential savings if red meat reduced by 50%
    const currentRedMeat = meatDist.red_meat_percent / 100;
    const savingPerMeal = (currentRedMeat * 0.5 * PROTEIN_CO2.red_meat * PORTION_SIZES.protein);
    const annualSavingTons = (savingPerMeal * annualMeals) / 1000;
    return annualSavingTons * CO2_COST_PER_TON_DKK;
}

/**
 * Generate smart recommendations based on current setup
 */
function generateRecommendations(meatDist, wastePercent, seasonalPercent, annualMeals, co2PerMeal) {
    const recs = [];

    // Recommendation 1: Reduce red meat
    if (meatDist.red_meat_percent > 15) {
        const currentRed = meatDist.red_meat_percent / 100;
        const savingPerMeal = (currentRed * 0.5 * PROTEIN_CO2.red_meat * PORTION_SIZES.protein);
        const annualSaving = (savingPerMeal * annualMeals) / 1000;
        recs.push({
            priority: 1,
            title: "Reducér Rødt Kød med 50%",
            description: `I har ${meatDist.red_meat_percent}% rødt kød. En halvering vil give betydelig CO2-reduktion uden at fjerne det helt fra menuen.`,
            annual_saving_tons: annualSaving,
            implementation_time: "3-6 måneder",
            difficulty: "Middel"
        });
    }

    // Recommendation 2: Increase vegetarian
    if (meatDist.vegetarian_percent < 30) {
        const increase = 0.20; // 20% increase
        const savingPerMeal = increase * (PROTEIN_CO2.bright_meat - PROTEIN_CO2.vegetarian) * PORTION_SIZES.protein;
        const annualSaving = (savingPerMeal * annualMeals) / 1000;
        recs.push({
            priority: 2,
            title: "Øg Vegetariske Retter til 30%",
            description: `Plantebaserede proteiner har kun ~2kg CO2e/kg mod 9-42kg for kød. Introducer attraktive vegetariske alternativer.`,
            annual_saving_tons: annualSaving,
            implementation_time: "2-4 måneder",
            difficulty: "Let"
        });
    }

    // Recommendation 3: Waste reduction
    if (wastePercent > 10) {
        const wasteReduction = wastePercent - 5; // Target 5%
        const savingPerMeal = co2PerMeal * (wasteReduction / 100);
        const annualSaving = (savingPerMeal * annualMeals) / 1000;
        recs.push({
            priority: 3,
            title: "Reducér Madspild til Under 5%",
            description: `Jeres madspild er ${wastePercent.toFixed(1)}%. Implementer portionskontrol og buffetoptimering.`,
            annual_saving_tons: annualSaving,
            implementation_time: "1-3 måneder",
            difficulty: "Let"
        });
    }

    // Recommendation 4: Seasonal produce
    if (seasonalPercent < 70) {
        const increase = (70 - seasonalPercent) / 100;
        const savingPerMeal = co2PerMeal * increase * SEASONAL_BENEFIT;
        const annualSaving = (savingPerMeal * annualMeals) / 1000;
        recs.push({
            priority: 4,
            title: "Øg Sæsonvarer til 70%",
            description: `Sæsonvarer reducerer transport og køleemissioner med op til 15%. Samarbejd med lokale leverandører.`,
            annual_saving_tons: annualSaving,
            implementation_time: "3-6 måneder",
            difficulty: "Middel"
        });
    }

    // Recommendation 5: Meat-free day
    const meatFreeDaySaving = (co2PerMeal * 0.6 * annualMeals * (1/5)) / 1000; // 60% of emissions, 1 day/week
    recs.push({
        priority: 5,
        title: "Introducér 'Grøn Mandag'",
        description: `En ugentlig kødfri dag kan reducere årsemissioner markant. Start med en dag og mål responsen.`,
        annual_saving_tons: meatFreeDaySaving,
        implementation_time: "1 måned",
        difficulty: "Let"
    });

    // Sort by impact and return top 5
    return recs.sort((a, b) => b.annual_saving_tons - a.annual_saving_tons).slice(0, 5);
}

/**
 * Format number with Danish locale
 */
function formatNumber(num, decimals = 2) {
    return num.toFixed(decimals).replace('.', ',');
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        calculateCanteenImpact,
        CO2_FACTORS,
        PROTEIN_CO2,
        formatNumber
    };
}
