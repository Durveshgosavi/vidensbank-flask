# Action Plan: Advanced Canteen Climate Analysis Tool

## 🎯 Objective
Build a production-ready canteen climate analysis tool that integrates:
- Real canteen database with 70+ Danish canteens
- Weekly menu planning and CO2 tracking
- Baseline comparison from actual data
- Advanced scenario testing
- Procurement, waste, and energy optimization

## 📋 Implementation Phases

### Phase 1: Database Enhancement ✅
**Status:** In Progress
**Tasks:**
1. ✅ Create canteen database schema
2. ✅ Import 70+ real canteen data
3. ✅ Add baseline metrics per canteen
4. ✅ Create weekly menu structure
5. ⏳ Add historical tracking

### Phase 2: Backend Enhancement
**Status:** Starting Now
**Tasks:**
1. Create CanteenProfile model with historical data
2. Build WeeklyMenuPlanner engine
3. Implement BaselineComparison calculator
4. Add ScenarioTester with multiple scenarios
5. Create advanced API endpoints

### Phase 3: Frontend Implementation
**Status:** Planned
**Tasks:**
1. Build canteen selection dropdown with search
2. Create weekly menu grid (Monday-Friday)
3. Implement detailed procurement controls
4. Add waste management initiatives UI
5. Build scenario testing interface
6. Create weekly CO2 tracker visualization

### Phase 4: Integration & Testing
**Status:** Planned
**Tasks:**
1. Connect to Power BI datawarehouse (when ready)
2. Test with real canteen data
3. Performance optimization
4. User acceptance testing
5. Deploy to production

### Phase 5: Advanced Features
**Status:** Future
**Tasks:**
1. AI-powered menu suggestions
2. Automatic baseline updates
3. Benchmarking against similar canteens
4. Export reports (PDF, Excel)
5. Email notifications for targets

## 🛠️ Technical Stack

**Backend:**
- Python 3.12
- Flask 3.0
- SQLAlchemy ORM
- SQLite (dev) / PostgreSQL (prod)

**Frontend:**
- Vanilla JavaScript (no framework dependencies)
- Bootstrap 5.3
- Chart.js for visualizations
- Font Awesome icons

**Data Sources:**
- CONCITO 2021 climate database
- Cheval Blanc canteen baseline data
- Power BI datawarehouse (future)

## 📊 Key Features

### 1. Canteen Selection System
- Searchable dropdown with 70+ canteens
- Auto-fill from baseline data
- Location-based filtering
- Recent selections memory

### 2. Weekly Menu Planning
- Monday-Friday menu grid
- Meat dish selection (beef, pork, chicken, fish, mixed)
- Green dish selection (vegan, legumes, dairy, egg)
- Portion size controls
- Dish distribution slider (meat vs green)

### 3. Baseline Comparison
- Show current canteen metrics
- CO2 per kg
- Green content %
- Organic %
- Food waste %
- Local sourcing %

### 4. Procurement & Transport
- Danish vs EU vs Global sourcing
- Organic percentages
- Seasonal produce tracking
- Transport distance calculation
- Air freight impact
- Direct farm purchases

### 5. Waste Management
- Three waste types: prep, plate, buffet
- Five waste reduction initiatives:
  - Pre-ordering from guests
  - Flexible portions (S/M/L)
  - Compost/biogas system
  - Daily waste tracking
  - Stock utilization

### 6. Energy Efficiency
- Cooking method (electric, gas, mixed)
- Equipment energy class (A, B, C)
- Batch cooking optimization

### 7. Scenario Testing
- Meatless Monday
- 100% Danish meat
- Reduce portions 10%
- All organic
- Zero waste target
- Custom scenarios

### 8. Weekly CO2 Tracking
- Bar chart showing daily emissions
- Identify high-impact days
- Visual comparison
- Trend analysis

## 🎨 User Experience Flow

```
1. User lands on Advanced Calculator page
   ↓
2. Searches and selects their canteen
   ↓
3. Baseline data auto-fills form
   ↓
4. User reviews/adjusts weekly menu
   ↓
5. User tweaks procurement, waste, energy settings
   ↓
6. Calculator shows real-time results:
   - Current vs optimized CO2
   - Annual savings potential
   - Cost savings estimate
   - Top 5 AI recommendations
   ↓
7. User tests different scenarios
   ↓
8. User exports action plan
   ↓
9. User tracks progress over time
```

## 📈 Success Metrics

**Immediate (MVP):**
- ✅ 70+ canteens in database
- ✅ <2 second calculation time
- ✅ Mobile responsive design
- ⏳ 95% accurate CO2 calculations

**Short-term (3 months):**
- 100+ active users
- 500+ calculations performed
- 10+ tons CO2 saved (verified)
- User satisfaction >4.5/5

**Long-term (1 year):**
- Integration with all Cheval Blanc canteens
- Real-time Power BI data sync
- Automated reporting
- 100+ tons CO2 saved annually

## 🔐 Security & Privacy

- No personal data collection
- Aggregated analytics only
- GDPR compliant
- Secure API endpoints
- Rate limiting
- Input validation

## 🚀 Deployment Strategy

**Development:**
- Local Flask server
- SQLite database
- Debug mode enabled

**Staging:**
- Heroku staging app
- PostgreSQL database
- Real data testing

**Production:**
- Heroku production app
- Scheduled backups
- Performance monitoring
- Error tracking (Sentry)

## 📝 Documentation

**User Documentation:**
- Getting started guide
- Video tutorials
- FAQ section
- Best practices

**Developer Documentation:**
- API reference
- Database schema
- Calculation methodology
- Contributing guidelines

## 🔄 Maintenance Plan

**Weekly:**
- Monitor performance
- Review user feedback
- Update canteen data

**Monthly:**
- Update CONCITO data if available
- Add new features
- Performance optimization

**Quarterly:**
- Major feature releases
- User training sessions
- Impact reporting

## 💡 Innovation Opportunities

1. **Machine Learning:**
   - Predict optimal menu combinations
   - Forecast seasonal trends
   - Anomaly detection in waste patterns

2. **Gamification:**
   - Canteen leaderboards
   - Achievement badges
   - CO2 reduction challenges

3. **Integration:**
   - Recipe databases
   - Supplier catalogs
   - Nutrition analysis

4. **Advanced Analytics:**
   - Multi-year trend analysis
   - Peer benchmarking
   - Predictive modeling

---

**Last Updated:** 2025-11-13
**Version:** 1.0
**Status:** Phase 2 in progress
