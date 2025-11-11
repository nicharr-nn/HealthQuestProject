<template>
  <div class="min-h-screen bg-slate-50 text-slate-900 font-subtitle">
    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-40 bg-black/40 md:hidden"
      @click="sidebarOpen = false"
    />

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-50 w-72 bg-slate-900 text-white transition-transform duration-300 md:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
      aria-label="Sidebar"
    >
      <div class="px-6 pb-6 pt-8 border-b border-white/10">
        <h1 class="text-xl font-bold text-blue-400">HealthQuest Admin</h1>
      </div>

      <nav class="px-2 py-6 space-y-8 overflow-y-auto h-[calc(100vh-88px)]">
        <div v-for="group in nav" :key="group.title" class="space-y-2">
          <div class="px-4 text-[11px] font-semibold tracking-wider uppercase text-slate-400">
            {{ group.title }}
          </div>

          <a
            v-for="item in group.items"
            :key="item.id"
            href="#"
            class="group flex items-center gap-3 rounded-md px-4 py-2.5 text-slate-300 hover:text-blue-400 hover:bg-blue-500/10 border-r-2 border-transparent"
            :class="activeSection === item.id ? 'bg-blue-500/10 text-blue-400 border-blue-500' : ''"
            @click.prevent="setSection(item.id)"
          >
            <span class="w-5 h-5 shrink-0">{{ item.icon }}</span>
            <span class="truncate">{{ item.label }}</span>
            <span
              v-if="item.badge"
              class="ml-auto rounded-full px-2 py-0.5 text-[11px] font-medium bg-rose-500 text-white"
            >
              {{ item.badge }}
            </span>
          </a>
        </div>
      </nav>
    </aside>

    <!-- Main column -->
    <div class="md:pl-72">
      <!-- Header -->
      <header class="sticky top-0 z-30 bg-white/90 backdrop-blur supports-[backdrop-filter]:bg-white/60 shadow-sm">
        <div class="flex items-center justify-between px-4 py-3 md:px-8">
          <div class="flex items-center gap-3">
            <button
              class="inline-flex md:hidden items-center justify-center rounded-md p-2 text-slate-700 hover:bg-slate-100"
              @click="sidebarOpen = !sidebarOpen"
              aria-label="Toggle menu"
            >
              ☰
            </button>

            <div class="relative hidden md:block">
              <span class="absolute left-3 top-1/2 -translate-y-1/2">🔍</span>
              <input
                type="text"
                placeholder="Search coaches..."
                v-model="searchQuery"
                class="w-80 rounded-md border border-slate-200 pl-9 pr-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
              />
            </div>
          </div>

          <div class="flex items-center gap-3">
            <button
              class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700"
              @click="goBackToApp"
            >
              Back to App
            </button>
            <button class="relative rounded-md bg-slate-100 p-2" @click="showNotifications">
              🔔
              <span v-if="pendingCount > 0" class="absolute right-1 top-1 inline-block h-2 w-2 rounded-full bg-rose-500"></span>
            </button>
            <div class="flex items-center gap-2">
              <div class="grid h-10 w-10 place-items-center rounded-full bg-blue-500 font-bold text-white">A</div>
              <div class="leading-tight">
                <div class="font-medium">{{ userStore.profile?.user?.username || 'Admin' }}</div>
                <div class="text-[11px] text-slate-500">Administrator</div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="px-4 py-6 md:px-8">
        <!-- COACHES CERTIFICATION SECTION -->
        <section v-show="activeSection === 'coaches'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">Coach Certification Verification</h2>
            <p class="text-sm text-slate-500">Review and verify coach certifications</p>
          </div>

          <!-- Backend API Notice -->
          <div class="rounded-xl bg-amber-50 border border-amber-200 p-4">
            <div class="flex items-start gap-3">
              <span class="text-2xl">⚠️</span>
              <div class="flex-1">
                <h4 class="font-semibold text-amber-900">Backend API Required</h4>
                <p class="text-sm text-amber-800 mt-1">
                  To fully implement coach certification verification, the following backend endpoints are needed:
                </p>
                <ul class="text-sm text-amber-800 mt-2 list-disc list-inside space-y-1">
                  <li><code class="bg-amber-100 px-1 rounded">GET /api/admin/coaches/</code> - List all coaches with filters</li>
                  <li><code class="bg-amber-100 px-1 rounded">POST /api/admin/coaches/{id}/approve/</code> - Approve certification</li>
                  <li><code class="bg-amber-100 px-1 rounded">POST /api/admin/coaches/{id}/reject/</code> - Reject certification</li>
                </ul>
                <p class="text-sm text-amber-800 mt-2">Currently showing demonstration with mock data.</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">Coach Applications</h3>
              <div class="flex items-center gap-3">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="coachFilter">
                  <option value="all">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
                <button class="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700" @click="exportCoachList">
                  Export List
                </button>
              </div>
            </div>

            <div v-if="loading" class="text-center py-8 text-slate-500">
              Loading coaches...
            </div>

            <div v-else-if="error" class="text-center py-8 text-rose-600">
              {{ error }}
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-semibold">Coach Name</th>
                    <th class="px-3 py-2 text-left font-semibold">Email</th>
                    <th class="px-3 py-2 text-left font-semibold">Bio</th>
                    <th class="px-3 py-2 text-left font-semibold">Applied Date</th>
                    <th class="px-3 py-2 text-left font-semibold">Status</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredCoaches.length === 0">
                    <td colspan="6" class="px-3 py-8 text-center text-slate-500">
                      No coaches found{{ coachFilter !== 'all' ? ' with status: ' + coachFilter : '' }}
                    </td>
                  </tr>
                  <tr
                    v-for="coach in filteredCoaches"
                    :key="coach.coach_id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-2">
                        <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">
                          {{ getInitials(coach.name) }}
                        </div>
                        {{ coach.name }}
                      </div>
                    </td>
                    <td class="px-3 py-3">{{ coach.email || 'N/A' }}</td>
                    <td class="px-3 py-3">
                      <div class="max-w-xs truncate">{{ coach.bio || 'No bio provided' }}</div>
                    </td>
                    <td class="px-3 py-3">{{ formatDate(coach.created_at) }}</td>
                    <td class="px-3 py-3">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                        :class="getStatusClass(coach.status_approval)"
                      >
                        {{ coach.status_approval }}
                      </span>
                    </td>
                    <td class="px-3 py-3">
                      <button
                        class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700"
                        @click="viewCoachDetails(coach)"
                      >
                        Review
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- DASHBOARD SECTION -->
        <section v-show="activeSection === 'dashboard'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">Dashboard</h2>
            <p class="text-sm text-slate-500">Overview of platform statistics</p>
          </div>

          <!-- Stats Cards -->
          <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-slate-600">Total Users</p>
                  <p class="text-3xl font-bold text-slate-900">{{ userStats.total }}</p>
                </div>
                <div class="grid h-12 w-12 place-items-center rounded-full bg-blue-100 text-2xl">👥</div>
              </div>
              <p class="mt-2 text-xs text-emerald-600">+{{ userStats.newThisMonth }} this month</p>
            </div>

            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-slate-600">Active Coaches</p>
                  <p class="text-3xl font-bold text-slate-900">{{ userStats.coaches }}</p>
                </div>
                <div class="grid h-12 w-12 place-items-center rounded-full bg-emerald-100 text-2xl">🏃</div>
              </div>
              <p class="mt-2 text-xs text-slate-600">{{ userStats.pendingCoaches }} pending approval</p>
            </div>

            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-slate-600">Total Recipes</p>
                  <p class="text-3xl font-bold text-slate-900">{{ recipeStats.total }}</p>
                </div>
                <div class="grid h-12 w-12 place-items-center rounded-full bg-amber-100 text-2xl">🍽️</div>
              </div>
              <p class="mt-2 text-xs text-rose-600">{{ recipeStats.pendingReview }} need review</p>
            </div>

            <div class="rounded-xl bg-white p-5 shadow-sm">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm text-slate-600">Member Requests</p>
                  <p class="text-3xl font-bold text-slate-900">{{ memberStats.pending }}</p>
                </div>
                <div class="grid h-12 w-12 place-items-center rounded-full bg-purple-100 text-2xl">📋</div>
              </div>
              <p class="mt-2 text-xs text-slate-600">{{ memberStats.total }} total members</p>
            </div>
          </div>

          <!-- User Growth Chart -->
          <div class="rounded-xl bg-white p-5 shadow-sm">
            <h3 class="mb-4 text-base font-semibold">User Growth (Last 6 Months)</h3>
            <div class="h-80">
              <Line :data="chartData" :options="chartOptions" />
            </div>
          </div>

          <!-- User Distribution by Role -->
          <div class="grid gap-6 md:grid-cols-2">
            <div class="rounded-xl bg-white p-5 shadow-sm">
              <h3 class="mb-4 text-base font-semibold">User Distribution by Role</h3>
              <div class="h-64">
                <Doughnut :data="roleChartData" :options="doughnutOptions" />
              </div>
            </div>

            <div class="rounded-xl bg-white p-5 shadow-sm">
              <h3 class="mb-4 text-base font-semibold">User Distribution by Gender</h3>
              <div class="h-64">
                <Doughnut :data="genderChartData" :options="doughnutOptions" />
              </div>
            </div>
          </div>
        </section>

        <!-- USERS SECTION -->
        <section v-show="activeSection === 'users'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">User Management</h2>
            <p class="text-sm text-slate-500">View and manage user accounts</p>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">All Users</h3>
              <div class="flex items-center gap-3">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="userRoleFilter">
                  <option value="all">All Roles</option>
                  <option value="normal">Normal Users</option>
                  <option value="coach">Coaches</option>
                  <option value="member">Members</option>
                </select>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2">🔍</span>
                  <input
                    type="text"
                    placeholder="Search users..."
                    v-model="userSearchQuery"
                    class="rounded-md border border-slate-200 pl-9 pr-3 py-2 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                  />
                </div>
              </div>
            </div>

            <div v-if="loadingUsers" class="text-center py-8 text-slate-500">
              Loading users...
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-semibold">User</th>
                    <th class="px-3 py-2 text-left font-semibold">Email</th>
                    <th class="px-3 py-2 text-left font-semibold">Role</th>
                    <th class="px-3 py-2 text-left font-semibold">Level</th>
                    <th class="px-3 py-2 text-left font-semibold">Joined</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredUsers.length === 0">
                    <td colspan="6" class="px-3 py-8 text-center text-slate-500">
                      No users found
                    </td>
                  </tr>
                  <tr
                    v-for="user in filteredUsers"
                    :key="user.id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-2">
                        <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">
                          {{ getInitials(user.username) }}
                        </div>
                        {{ user.username }}
                      </div>
                    </td>
                    <td class="px-3 py-3">{{ user.email || 'N/A' }}</td>
                    <td class="px-3 py-3">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                        :class="getRoleClass(user.role)"
                      >
                        {{ user.role }}
                      </span>
                    </td>
                    <td class="px-3 py-3">
                      <span class="text-xs text-slate-600">
                        {{ user.level || 'Bronze' }} ({{ user.xp || 0 }} XP)
                      </span>
                    </td>
                    <td class="px-3 py-3">{{ formatDate(user.created_at) }}</td>
                    <td class="px-3 py-3">
                      <div class="flex gap-2">
                        <button
                          class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs"
                          @click="viewUserDetails(user)"
                        >
                          View
                        </button>
                        <button
                          class="rounded-md bg-rose-600 px-3 py-1.5 text-white hover:bg-rose-700 text-xs"
                          @click="confirmDeleteUser(user)"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- RECIPES SECTION -->
        <section v-show="activeSection === 'recipes'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">Recipe Management</h2>
            <p class="text-sm text-slate-500">View and manage all recipes posted on the platform</p>
          </div>

          <!-- Backend API Connected Notice -->
          <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4">
            <div class="flex items-start gap-3">
              <span class="text-2xl">✓</span>
              <div class="flex-1">
                <h4 class="font-semibold text-emerald-900">Connected to Backend API</h4>
                <p class="text-sm text-emerald-800 mt-1">
                  Recipe management is now connected to the live backend API.
                </p>
                <ul class="text-sm text-emerald-800 mt-2 list-disc list-inside space-y-1">
                  <li><code class="bg-emerald-100 px-1 rounded">GET /api/recipe/</code> - List all recipes</li>
                  <li><code class="bg-emerald-100 px-1 rounded">DELETE /api/recipe/{id}/delete/</code> - Delete recipe</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">All Recipes ({{ recipes.length }})</h3>
              <div class="flex items-center gap-3">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="recipeAccessFilter">
                  <option value="all">All Access Levels</option>
                  <option value="silver">Silver</option>
                  <option value="gold">Gold</option>
                </select>
              </div>
            </div>

            <div v-if="loadingRecipes" class="text-center py-8 text-slate-500">
              Loading recipes...
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-semibold">Recipe</th>
                    <th class="px-3 py-2 text-left font-semibold">Author</th>
                    <th class="px-3 py-2 text-left font-semibold">Access Level</th>
                    <th class="px-3 py-2 text-left font-semibold">Created</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredRecipes.length === 0">
                    <td colspan="5" class="px-3 py-8 text-center text-slate-500">
                      No recipes found
                    </td>
                  </tr>
                  <tr
                    v-for="recipe in filteredRecipes"
                    :key="recipe.id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-3">
                        <div v-if="recipe.image" class="h-12 w-12 rounded-md bg-slate-200 overflow-hidden">
                          <img :src="recipe.image" :alt="recipe.title" class="h-full w-full object-cover" />
                        </div>
                        <div v-else class="grid h-12 w-12 place-items-center rounded-md bg-amber-100 text-xl">
                          🍽️
                        </div>
                        <div>
                          <div class="font-medium">{{ recipe.title }}</div>
                          <div class="text-xs text-slate-500">{{ getIngredientCount(recipe.ingredients) }} ingredients</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-3 py-3">{{ recipe.author }}</td>
                    <td class="px-3 py-3">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                        :class="recipe.access_level === 'gold' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-800'"
                      >
                        {{ recipe.access_level }}
                      </span>
                    </td>
                    <td class="px-3 py-3">{{ formatDate(recipe.created_at) }}</td>
                    <td class="px-3 py-3">
                      <div class="flex gap-2">
                        <button
                          class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs"
                          @click="viewRecipeDetails(recipe)"
                        >
                          View
                        </button>
                        <button
                          class="rounded-md bg-rose-600 px-3 py-1.5 text-white hover:bg-rose-700 text-xs"
                          @click="deleteRecipe(recipe)"
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- WORKOUTS SECTION -->
        <section v-show="activeSection === 'workouts'" class="space-y-6">
          <div>
            <h2 class="text-2xl font-bold">Workout Management</h2>
            <p class="text-sm text-slate-500">View all workout programs and their associated coaches</p>
          </div>

          <!-- Backend API Connected Notice -->
          <div class="rounded-xl bg-emerald-50 border border-emerald-200 p-4">
            <div class="flex items-start gap-3">
              <span class="text-2xl">✓</span>
              <div class="flex-1">
                <h4 class="font-semibold text-emerald-900">Connected to Backend API</h4>
                <p class="text-sm text-emerald-800 mt-1">
                  Workout management is now connected to the live backend API.
                </p>
                <ul class="text-sm text-emerald-800 mt-2 list-disc list-inside space-y-1">
                  <li><code class="bg-emerald-100 px-1 rounded">GET /api/workout/programs/</code> - List all workout programs</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="rounded-xl bg-white p-5 shadow-sm">
            <div class="mb-4 flex items-center justify-between">
              <h3 class="text-base font-semibold">All Workout Programs ({{ workouts.length }})</h3>
              <div class="flex items-center gap-3">
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="workoutCategoryFilter">
                  <option value="all">All Categories</option>
                  <option value="strength_training">Strength Training</option>
                  <option value="cardio">Cardio</option>
                  <option value="weight_loss">Weight Loss</option>
                  <option value="muscle_building">Muscle Building</option>
                  <option value="endurance">Endurance</option>
                  <option value="flexibility">Flexibility</option>
                  <option value="full_body">Full Body</option>
                </select>
                <select class="rounded-md border border-slate-200 px-3 py-2 text-sm" v-model="workoutDifficultyFilter">
                  <option value="all">All Difficulties</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
            </div>

            <div v-if="loadingWorkouts" class="text-center py-8 text-slate-500">
              Loading workouts...
            </div>

            <div v-else class="overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead class="text-slate-500">
                  <tr class="border-b border-slate-200">
                    <th class="px-3 py-2 text-left font-semibold">Program Title</th>
                    <th class="px-3 py-2 text-left font-semibold">Coach</th>
                    <th class="px-3 py-2 text-left font-semibold">Category</th>
                    <th class="px-3 py-2 text-left font-semibold">Difficulty</th>
                    <th class="px-3 py-2 text-left font-semibold">Duration</th>
                    <th class="px-3 py-2 text-left font-semibold">Days</th>
                    <th class="px-3 py-2 text-left font-semibold">Created</th>
                    <th class="px-3 py-2 text-left font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredWorkouts.length === 0">
                    <td colspan="8" class="px-3 py-8 text-center text-slate-500">
                      No workout programs found
                    </td>
                  </tr>
                  <tr
                    v-for="workout in filteredWorkouts"
                    :key="workout.id"
                    class="border-b border-slate-100 hover:bg-slate-50"
                  >
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-2">
                        <div class="grid h-8 w-8 place-items-center rounded-md bg-blue-100 text-lg">
                          💪
                        </div>
                        <div>
                          <div class="font-medium">{{ workout.title }}</div>
                          <div class="text-xs text-slate-500 truncate max-w-xs">{{ workout.description }}</div>
                        </div>
                      </div>
                    </td>
                    <td class="px-3 py-3">
                      <div class="flex items-center gap-2">
                        <div class="grid h-6 w-6 place-items-center rounded-full bg-emerald-500 text-xs font-bold text-white">
                          {{ getInitials(workout.coach_name) }}
                        </div>
                        <span>{{ workout.coach_name }}</span>
                      </div>
                    </td>
                    <td class="px-3 py-3">
                      <span class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize bg-purple-100 text-purple-800">
                        {{ formatCategory(workout.category) }}
                      </span>
                    </td>
                    <td class="px-3 py-3">
                      <span
                        class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                        :class="getDifficultyClass(workout.difficulty_level)"
                      >
                        {{ workout.difficulty_level }}
                      </span>
                    </td>
                    <td class="px-3 py-3">{{ workout.duration }} days</td>
                    <td class="px-3 py-3">{{ workout.days?.length || 0 }} days</td>
                    <td class="px-3 py-3">{{ formatDate(workout.created_at) }}</td>
                    <td class="px-3 py-3">
                      <button
                        class="rounded-md bg-blue-600 px-3 py-1.5 text-white hover:bg-blue-700 text-xs"
                        @click="viewWorkoutDetails(workout)"
                      >
                        View
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </main>
    </div>

    <!-- Coach Review Modal -->
    <div
      v-if="coachModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeCoachModal"
    >
      <div class="w-full max-w-2xl overflow-hidden rounded-xl bg-white shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-semibold">Coach Certification Review</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeCoachModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-sm font-medium text-slate-700">Coach Name</div>
              <div class="text-base">{{ coachModal.coach?.name }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Email</div>
              <div class="text-base">{{ coachModal.coach?.email || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Applied Date</div>
              <div class="text-base">{{ formatDate(coachModal.coach?.created_at) }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Current Status</div>
              <div>
                <span
                  class="rounded-full px-2 py-1 text-xs font-medium capitalize"
                  :class="getStatusClass(coachModal.coach?.status_approval)"
                >
                  {{ coachModal.coach?.status_approval }}
                </span>
              </div>
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Bio</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md">
              {{ coachModal.coach?.bio || 'No bio provided' }}
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Certification Document</div>
            <div v-if="coachModal.coach?.certification_doc" class="border border-slate-200 rounded-md p-4">
              <div class="flex items-center gap-3">
                <span class="text-3xl">📄</span>
                <div class="flex-1">
                  <div class="text-sm font-medium">Certification Document</div>
                  <div class="text-xs text-slate-500">{{ coachModal.coach.certification_doc }}</div>
                </div>
                <a
                  :href="getDocumentUrl(coachModal.coach.certification_doc)"
                  target="_blank"
                  class="rounded-md bg-blue-600 px-3 py-1.5 text-sm text-white hover:bg-blue-700"
                >
                  View PDF
                </a>
              </div>
            </div>
            <div v-else class="text-sm text-slate-500 italic">
              No certification document uploaded
            </div>
          </div>

          <div v-if="coachModal.coach?.status_approval === 'pending'" class="bg-blue-50 border border-blue-200 rounded-md p-4">
            <div class="text-sm font-medium text-blue-900 mb-2">Verification Checklist</div>
            <ul class="text-sm text-blue-800 space-y-1">
              <li>✓ Verify certification document is valid and current</li>
              <li>✓ Check coach credentials match the information provided</li>
              <li>✓ Ensure bio is professional and appropriate</li>
              <li>✓ Confirm coach meets platform requirements</li>
            </ul>
          </div>
        </div>

        <div class="flex justify-between items-center gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <div class="text-xs text-slate-500">
            Reviewing: {{ coachModal.coach?.name }}
          </div>
          <div class="flex gap-2">
            <button
              class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
              @click="closeCoachModal"
            >
              Cancel
            </button>
            <button
              v-if="coachModal.coach?.status_approval !== 'rejected'"
              class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700"
              @click="rejectCoach(coachModal.coach)"
            >
              Reject
            </button>
            <button
              v-if="coachModal.coach?.status_approval !== 'approved'"
              class="rounded-md bg-emerald-600 px-4 py-2 text-white hover:bg-emerald-700"
              @click="approveCoach(coachModal.coach)"
            >
              Approve Certification
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div
      v-if="userModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeUserModal"
    >
      <div class="w-full max-w-2xl overflow-hidden rounded-xl bg-white shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-semibold">User Profile Details</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeUserModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-sm font-medium text-slate-700">Username</div>
              <div class="text-base">{{ userModal.user?.username }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Email</div>
              <div class="text-base">{{ userModal.user?.email || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Role</div>
              <div>
                <span
                  class="rounded-full px-2 py-1 text-xs font-medium capitalize"
                  :class="getRoleClass(userModal.user?.role)"
                >
                  {{ userModal.user?.role }}
                </span>
              </div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Level</div>
              <div class="text-base">{{ userModal.user?.level || 'Bronze' }} ({{ userModal.user?.xp || 0 }} XP)</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Gender</div>
              <div class="text-base">{{ userModal.user?.gender || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Age</div>
              <div class="text-base">{{ userModal.user?.age || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Height</div>
              <div class="text-base">{{ userModal.user?.height ? userModal.user.height + ' cm' : 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Weight</div>
              <div class="text-base">{{ userModal.user?.weight ? userModal.user.weight + ' kg' : 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Location</div>
              <div class="text-base">{{ userModal.user?.location || 'N/A' }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Joined Date</div>
              <div class="text-base">{{ formatDate(userModal.user?.created_at) }}</div>
            </div>
          </div>

          <div v-if="userModal.user?.fitness_goals?.length">
            <div class="text-sm font-medium text-slate-700 mb-2">Fitness Goals</div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="goal in userModal.user.fitness_goals"
                :key="goal"
                class="rounded-full bg-blue-100 px-3 py-1 text-xs text-blue-800"
              >
                {{ goal }}
              </span>
            </div>
          </div>

          <div v-if="userModal.user?.achievements?.length">
            <div class="text-sm font-medium text-slate-700 mb-2">Achievements</div>
            <div class="space-y-2">
              <div
                v-for="achievement in userModal.user.achievements"
                :key="achievement.title"
                class="flex items-center gap-2 rounded-md bg-amber-50 p-2"
              >
                <span class="text-xl">🏆</span>
                <div>
                  <div class="text-sm font-medium">{{ achievement.title }}</div>
                  <div class="text-xs text-slate-600">+{{ achievement.xp_reward }} XP</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <button
            class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
            @click="closeUserModal"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Recipe Review Modal -->
    <div
      v-if="recipeModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeRecipeModal"
    >
      <div class="w-full max-w-3xl overflow-hidden rounded-xl bg-white shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-semibold">Recipe Safety Review</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeRecipeModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div v-if="recipeModal.recipe?.image" class="w-full h-48 rounded-lg bg-slate-200 overflow-hidden">
            <img :src="recipeModal.recipe.image" :alt="recipeModal.recipe.title" class="h-full w-full object-cover" />
          </div>

          <div>
            <h4 class="text-xl font-bold">{{ recipeModal.recipe?.title }}</h4>
            <div class="flex items-center gap-3 mt-2">
              <span class="text-sm text-slate-600">By {{ recipeModal.recipe?.author }}</span>
              <span
                class="rounded-full px-2 py-0.5 text-[11px] font-medium capitalize"
                :class="recipeModal.recipe?.access_level === 'gold' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-800'"
              >
                {{ recipeModal.recipe?.access_level }}
              </span>
              <div class="flex items-center gap-1">
                <span class="text-amber-500">⭐</span>
                <span class="text-sm">{{ recipeModal.recipe?.average_rating || 'N/A' }}</span>
              </div>
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Ingredients</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md whitespace-pre-line">
              {{ recipeModal.recipe?.ingredients }}
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Instructions</div>
            <div class="text-sm bg-slate-50 p-3 rounded-md whitespace-pre-line">
              {{ recipeModal.recipe?.steps }}
            </div>
          </div>

          <div>
            <div class="text-sm font-medium text-slate-700 mb-2">Recipe Details</div>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-slate-600">Access Level:</span>
                <span class="ml-2 capitalize font-medium">{{ recipeModal.recipe?.access_level }}</span>
              </div>
              <div>
                <span class="text-slate-600">Created:</span>
                <span class="ml-2 font-medium">{{ formatDate(recipeModal.recipe?.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-between items-center gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <div class="text-xs text-slate-500">
            Reviewing: {{ recipeModal.recipe?.title }}
          </div>
          <div class="flex gap-2">
            <button
              class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
              @click="closeRecipeModal"
            >
              Close
            </button>
            <button
              class="rounded-md bg-rose-600 px-4 py-2 text-white hover:bg-rose-700"
              @click="deleteRecipe(recipeModal.recipe)"
            >
              Delete Recipe
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Workout Details Modal -->
    <div
      v-if="workoutModal.open"
      class="fixed inset-0 z-[60] grid place-items-center bg-black/50 p-4"
      role="dialog"
      aria-modal="true"
      @click.self="closeWorkoutModal"
    >
      <div class="w-full max-w-3xl overflow-hidden rounded-xl bg-white shadow-lg">
        <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h3 class="text-lg font-semibold">Workout Program Details</h3>
          <button class="text-slate-500 hover:text-slate-700" @click="closeWorkoutModal">✕</button>
        </div>

        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <div>
            <h4 class="text-xl font-bold">{{ workoutModal.workout?.title }}</h4>
            <p class="text-sm text-slate-600 mt-2">{{ workoutModal.workout?.description }}</p>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <div class="text-sm font-medium text-slate-700">Coach</div>
              <div class="flex items-center gap-2 mt-1">
                <div class="grid h-8 w-8 place-items-center rounded-full bg-emerald-500 text-xs font-bold text-white">
                  {{ getInitials(workoutModal.workout?.coach_name) }}
                </div>
                <span class="text-base">{{ workoutModal.workout?.coach_name }}</span>
              </div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Category</div>
              <div class="text-base capitalize mt-1">{{ formatCategory(workoutModal.workout?.category) }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Difficulty Level</div>
              <div class="mt-1">
                <span
                  class="rounded-full px-2 py-1 text-xs font-medium capitalize"
                  :class="getDifficultyClass(workoutModal.workout?.difficulty_level)"
                >
                  {{ workoutModal.workout?.difficulty_level }}
                </span>
              </div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Duration</div>
              <div class="text-base mt-1">{{ workoutModal.workout?.duration }} days</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Level Access</div>
              <div class="text-base capitalize mt-1">{{ workoutModal.workout?.level_access }}</div>
            </div>
            <div>
              <div class="text-sm font-medium text-slate-700">Created</div>
              <div class="text-base mt-1">{{ formatDate(workoutModal.workout?.created_at) }}</div>
            </div>
          </div>

          <div v-if="workoutModal.workout?.days?.length">
            <div class="text-sm font-medium text-slate-700 mb-2">Workout Days ({{ workoutModal.workout.days.length }})</div>
            <div class="space-y-2 max-h-60 overflow-y-auto">
              <div
                v-for="day in workoutModal.workout.days"
                :key="day.id"
                class="flex items-center justify-between rounded-md bg-slate-50 p-3"
              >
                <div class="flex items-center gap-3">
                  <div class="grid h-8 w-8 place-items-center rounded-full bg-blue-500 text-xs font-bold text-white">
                    {{ day.day_number }}
                  </div>
                  <div>
                    <div class="text-sm font-medium">{{ day.title || `Day ${day.day_number}` }}</div>
                    <div class="text-xs text-slate-500">{{ day.duration }} minutes • {{ day.video_links?.length || 0 }} videos</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 border-t border-slate-200 px-5 py-4 bg-slate-50">
          <button
            class="rounded-md border border-slate-300 bg-white px-4 py-2 text-slate-700 hover:bg-slate-50"
            @click="closeWorkoutModal"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Line, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

const router = useRouter()
const userStore = useUserStore()
const sidebarOpen = ref(false)
const activeSection = ref('dashboard')
const coachFilter = ref('all')
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)

// User management state
const userRoleFilter = ref('all')
const userSearchQuery = ref('')
const loadingUsers = ref(false)

// Recipe management state
const recipeAccessFilter = ref('all')
const loadingRecipes = ref(false)

// Workout management state
const workoutCategoryFilter = ref('all')
const workoutDifficultyFilter = ref('all')
const loadingWorkouts = ref(false)
const workouts = ref([])

// Mock coaches data - In production, this would come from API
const coaches = ref([
  {
    coach_id: 1,
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    bio: 'Certified personal trainer with 5 years of experience in strength training and nutrition coaching.',
    certification_doc: 'coach_certifications/sarah_johnson_cert.pdf',
    status_approval: 'pending',
    created_at: '2024-09-10T10:30:00Z'
  },
  {
    coach_id: 2,
    name: 'Mike Rodriguez',
    email: 'mike.rodriguez@email.com',
    bio: 'Yoga instructor and mindfulness coach with RYT-500 certification. Specializing in holistic wellness.',
    certification_doc: 'coach_certifications/mike_rodriguez_cert.pdf',
    status_approval: 'approved',
    created_at: '2024-09-09T14:20:00Z',
    approved_date: '2024-09-10T09:15:00Z'
  },
  {
    coach_id: 3,
    name: 'Lisa Wang',
    email: 'lisa.wang@email.com',
    bio: 'Nutrition coach and registered dietitian. Helping clients achieve sustainable healthy eating habits.',
    certification_doc: 'coach_certifications/lisa_wang_cert.pdf',
    status_approval: 'pending',
    created_at: '2024-09-08T16:45:00Z'
  },
  {
    coach_id: 4,
    name: 'James Smith',
    email: 'james.smith@email.com',
    bio: 'CrossFit Level 2 trainer with focus on functional fitness and athletic performance.',
    certification_doc: 'coach_certifications/james_smith_cert.pdf',
    status_approval: 'rejected',
    created_at: '2024-09-05T11:00:00Z'
  }
])

const coachModal = ref({
  open: false,
  coach: null
})

// User modal state
const userModal = ref({
  open: false,
  user: null
})

// Recipe modal state
const recipeModal = ref({
  open: false,
  recipe: null
})

// Workout modal state
const workoutModal = ref({
  open: false,
  workout: null
})

// Mock users data
const users = ref([
  {
    id: 1,
    username: 'john_doe',
    email: 'john@example.com',
    role: 'normal',
    level: 'Gold',
    xp: 1250,
    gender: 'Male',
    age: 28,
    height: 178,
    weight: 75,
    location: 'New York, USA',
    created_at: '2024-08-15T10:30:00Z',
    fitness_goals: ['Lose Weight', 'Build Muscle'],
    achievements: [
      { title: 'First Workout', xp_reward: 100 },
      { title: 'Week Streak', xp_reward: 250 }
    ]
  },
  {
    id: 2,
    username: 'sarah_coach',
    email: 'sarah.johnson@email.com',
    role: 'coach',
    level: 'Platinum',
    xp: 2800,
    gender: 'Female',
    age: 32,
    height: 165,
    weight: 58,
    location: 'Los Angeles, USA',
    created_at: '2024-07-20T14:20:00Z',
    fitness_goals: ['Improve Endurance'],
    achievements: [
      { title: 'Certified Coach', xp_reward: 500 },
      { title: 'First Client', xp_reward: 300 }
    ]
  },
  {
    id: 3,
    username: 'mike_fit',
    email: 'mike@example.com',
    role: 'member',
    level: 'Silver',
    xp: 580,
    gender: 'Male',
    age: 24,
    height: 182,
    weight: 88,
    location: 'Chicago, USA',
    created_at: '2024-09-01T08:15:00Z',
    fitness_goals: ['Build Muscle', 'Improve Strength'],
    achievements: []
  },
  {
    id: 4,
    username: 'emma_health',
    email: 'emma@example.com',
    role: 'normal',
    level: 'Bronze',
    xp: 120,
    gender: 'Female',
    age: 26,
    height: 168,
    weight: 62,
    location: 'Seattle, USA',
    created_at: '2024-10-15T16:45:00Z',
    fitness_goals: ['Lose Weight'],
    achievements: [
      { title: 'First Login', xp_reward: 50 }
    ]
  },
  {
    id: 5,
    username: 'alex_runner',
    email: 'alex@example.com',
    role: 'normal',
    level: 'Gold',
    xp: 1580,
    gender: 'Other',
    age: 30,
    height: 175,
    weight: 70,
    location: 'Boston, USA',
    created_at: '2024-06-10T11:00:00Z',
    fitness_goals: ['Improve Endurance', 'Marathon Training'],
    achievements: [
      { title: '5K Runner', xp_reward: 200 },
      { title: 'Month Streak', xp_reward: 400 }
    ]
  }
])

// Recipes data - fetched from API
const recipes = ref([])

// Stats data
const userStats = ref({
  total: 1247,
  newThisMonth: 89,
  coaches: 34,
  pendingCoaches: 0
})

const recipeStats = ref({
  total: 156,
  pendingReview: 12
})

const memberStats = ref({
  total: 423,
  pending: 15
})

// Chart data
const chartData = computed(() => ({
  labels: ['June', 'July', 'August', 'September', 'October', 'November'],
  datasets: [
    {
      label: 'New Users',
      data: [45, 67, 82, 95, 108, 89],
      borderColor: 'rgb(59, 130, 246)',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4,
      fill: true
    },
    {
      label: 'Active Users',
      data: [320, 385, 456, 523, 612, 687],
      borderColor: 'rgb(16, 185, 129)',
      backgroundColor: 'rgba(16, 185, 129, 0.1)',
      tension: 0.4,
      fill: true
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true
    }
  }
}

const roleChartData = computed(() => ({
  labels: ['Normal Users', 'Coaches', 'Members', 'Admin'],
  datasets: [
    {
      data: [892, 34, 320, 1],
      backgroundColor: [
        'rgba(59, 130, 246, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(245, 158, 11, 0.8)'
      ],
      borderColor: [
        'rgb(59, 130, 246)',
        'rgb(16, 185, 129)',
        'rgb(139, 92, 246)',
        'rgb(245, 158, 11)'
      ],
      borderWidth: 2
    }
  ]
}))

const genderChartData = computed(() => ({
  labels: ['Male', 'Female', 'Other/Prefer not to say'],
  datasets: [
    {
      data: [612, 578, 57],
      backgroundColor: [
        'rgba(59, 130, 246, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(139, 92, 246, 0.8)'
      ],
      borderColor: [
        'rgb(59, 130, 246)',
        'rgb(236, 72, 153)',
        'rgb(139, 92, 246)'
      ],
      borderWidth: 2
    }
  ]
}))

const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    }
  }
}

const filteredCoaches = computed(() => {
  let result = coaches.value

  // Filter by status
  if (coachFilter.value !== 'all') {
    result = result.filter(c => c.status_approval === coachFilter.value)
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.name.toLowerCase().includes(query) ||
      c.email?.toLowerCase().includes(query) ||
      c.bio?.toLowerCase().includes(query)
    )
  }

  return result
})

const filteredUsers = computed(() => {
  let result = users.value

  // Filter by role
  if (userRoleFilter.value !== 'all') {
    result = result.filter(u => u.role === userRoleFilter.value)
  }

  // Filter by search query
  if (userSearchQuery.value) {
    const query = userSearchQuery.value.toLowerCase()
    result = result.filter(u =>
      u.username.toLowerCase().includes(query) ||
      u.email?.toLowerCase().includes(query)
    )
  }

  return result
})

const filteredRecipes = computed(() => {
  let result = recipes.value

  // Filter by access level
  if (recipeAccessFilter.value !== 'all') {
    result = result.filter(r => r.access_level === recipeAccessFilter.value)
  }

  return result
})

const filteredWorkouts = computed(() => {
  let result = workouts.value

  // Filter by category
  if (workoutCategoryFilter.value !== 'all') {
    result = result.filter(w => w.category === workoutCategoryFilter.value)
  }

  // Filter by difficulty
  if (workoutDifficultyFilter.value !== 'all') {
    result = result.filter(w => w.difficulty_level === workoutDifficultyFilter.value)
  }

  return result
})

const pendingCount = computed(() => {
  return coaches.value.filter(c => c.status_approval === 'pending').length
})

const nav = computed(() => [
  {
    title: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '📊' }
    ]
  },
  {
    title: 'User Management',
    items: [
      { id: 'users', label: 'Users', icon: '👥' },
      { id: 'coaches', label: 'Coaches', icon: '🏃', badge: pendingCount.value || null }
    ]
  },
  {
    title: 'Content Management',
    items: [
      { id: 'workouts', label: 'Workouts', icon: '💪' },
      { id: 'recipes', label: 'Recipes', icon: '🍽️' }
    ]
  }
])

function setSection(id) {
  activeSection.value = id
  if (window.innerWidth < 768) sidebarOpen.value = false
}

function goBackToApp() {
  router.push('/')
}

function getInitials(name) {
  if (!name) return '?'
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

function getStatusClass(status) {
  switch (status) {
    case 'pending':
      return 'bg-amber-100 text-amber-800'
    case 'approved':
      return 'bg-emerald-100 text-emerald-800'
    case 'rejected':
      return 'bg-rose-100 text-rose-800'
    default:
      return 'bg-slate-100 text-slate-800'
  }
}

function getDocumentUrl(doc) {
  if (!doc) return '#'
  // In production, this would be the full URL to the document
  return `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/media/${doc}`
}

function viewCoachDetails(coach) {
  coachModal.value = {
    open: true,
    coach: coach
  }
}

function closeCoachModal() {
  coachModal.value = {
    open: false,
    coach: null
  }
}

function approveCoach(coach) {
  // In production, this would make an API call to approve the coach
  // POST /api/admin/coaches/{coach.coach_id}/approve/

  console.log('Approving coach:', coach)

  // Update local state (demo only)
  const index = coaches.value.findIndex(c => c.coach_id === coach.coach_id)
  if (index !== -1) {
    coaches.value[index].status_approval = 'approved'
    coaches.value[index].approved_date = new Date().toISOString()
  }

  alert(`✓ Coach "${coach.name}" has been approved!\n\nIn production, this would:\n1. Update the database\n2. Send approval email to coach\n3. Grant coach permissions\n4. Log the action in audit trail`)

  closeCoachModal()
}

function rejectCoach(coach) {
  const reason = prompt('Please provide a reason for rejection (optional):')

  // In production, this would make an API call to reject the coach
  // POST /api/admin/coaches/{coach.coach_id}/reject/
  // Body: { reason: reason }

  console.log('Rejecting coach:', coach, 'Reason:', reason)

  // Update local state (demo only)
  const index = coaches.value.findIndex(c => c.coach_id === coach.coach_id)
  if (index !== -1) {
    coaches.value[index].status_approval = 'rejected'
    coaches.value[index].rejection_reason = reason
  }

  alert(`✗ Coach "${coach.name}" has been rejected.\n\nIn production, this would:\n1. Update the database\n2. Send rejection email to coach\n3. Log the action in audit trail\n4. Allow coach to resubmit`)

  closeCoachModal()
}

// User management functions
function viewUserDetails(user) {
  userModal.value = {
    open: true,
    user: user
  }
}

function closeUserModal() {
  userModal.value = {
    open: false,
    user: null
  }
}

function confirmDeleteUser(user) {
  const confirmed = confirm(
    `Are you sure you want to delete user "${user.username}"?\n\nThis action cannot be undone and will:\n1. Remove all user data\n2. Delete their recipes and workouts\n3. Remove achievement progress\n4. Cancel any active memberships`
  )

  if (confirmed) {
    deleteUser(user)
  }
}

function deleteUser(user) {
  // In production, this would make an API call to delete the user
  // DELETE /api/user/{user.id}/

  console.log('Deleting user:', user)

  // Update local state (demo only)
  const index = users.value.findIndex(u => u.id === user.id)
  if (index !== -1) {
    users.value.splice(index, 1)
    userStats.value.total -= 1
  }

  alert(`✓ User "${user.username}" has been deleted.\n\nIn production, this would:\n1. Delete user from database\n2. Remove all associated data\n3. Log the deletion in audit trail\n4. Send confirmation email`)
}

function getRoleClass(role) {
  switch (role) {
    case 'coach':
      return 'bg-emerald-100 text-emerald-800'
    case 'member':
      return 'bg-purple-100 text-purple-800'
    case 'admin':
      return 'bg-amber-100 text-amber-800'
    default:
      return 'bg-blue-100 text-blue-800'
  }
}

// Recipe management functions
function viewRecipeDetails(recipe) {
  recipeModal.value = {
    open: true,
    recipe: recipe
  }
}

function closeRecipeModal() {
  recipeModal.value = {
    open: false,
    recipe: null
  }
}

function getIngredientCount(ingredients) {
  if (!ingredients) return 0
  return ingredients.split('\n').filter(line => line.trim()).length
}

// Fetch recipes from API
async function fetchRecipes() {
  loadingRecipes.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/api/recipe/', {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch recipes')
    }

    const data = await response.json()

    // Transform data to include author name from user_profile
    recipes.value = data.map(recipe => ({
      ...recipe,
      author: recipe.user_profile || 'Unknown',
      status: 'verified', // Default status since backend doesn't have status field
      average_rating: recipe.average_rating || 'N/A'
    }))

    // Update recipe stats
    recipeStats.value.total = recipes.value.length
    recipeStats.value.pendingReview = recipes.value.filter(r => r.status === 'pending').length
  } catch (err) {
    console.error('Error fetching recipes:', err)
    error.value = 'Failed to load recipes'
  } finally {
    loadingRecipes.value = false
  }
}

// Delete recipe function
async function deleteRecipe(recipe) {
  const confirmed = confirm(
    `Are you sure you want to delete recipe "${recipe.title}"?\n\nThis action cannot be undone.`
  )

  if (!confirmed) return

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/recipe/${recipe.id}/delete/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Failed to delete recipe')
    }

    // Remove from local state
    const index = recipes.value.findIndex(r => r.id === recipe.id)
    if (index !== -1) {
      recipes.value.splice(index, 1)
      recipeStats.value.total -= 1
    }

    alert(`✓ Recipe "${recipe.title}" has been deleted successfully.`)
    closeRecipeModal()
  } catch (err) {
    console.error('Error deleting recipe:', err)
    alert('Failed to delete recipe. Please try again.')
  }
}

function exportCoachList() {
  alert('Exporting coach list as CSV - download would start here\n\nIn production, this would generate a CSV file with all coach data.')
}

function showNotifications() {
  alert(`${pendingCount.value} pending coach applications require review`)
}

// Workout management functions
async function fetchWorkouts() {
  loadingWorkouts.value = true
  try {
    const response = await fetch('http://127.0.0.1:8000/api/workout/programs/', {
      headers: {
        'Authorization': `Token ${userStore.token}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('Failed to fetch workouts')
    }

    const data = await response.json()

    // Transform data to include coach name
    workouts.value = await Promise.all(data.map(async workout => {
      // Fetch coach information
      let coachName = 'Unknown Coach'
      try {
        const coachResponse = await fetch(`http://127.0.0.1:8000/api/user-info/`, {
          headers: {
            'Authorization': `Token ${userStore.token}`,
            'Content-Type': 'application/json'
          }
        })
        if (coachResponse.ok) {
          const coachData = await coachResponse.json()
          // Find coach by workout.coach id
          coachName = `Coach ${workout.coach}`
        }
      } catch (err) {
        console.error('Error fetching coach info:', err)
      }

      return {
        ...workout,
        coach_name: coachName
      }
    }))
  } catch (err) {
    console.error('Error fetching workouts:', err)
    error.value = 'Failed to load workouts'
  } finally {
    loadingWorkouts.value = false
  }
}

function viewWorkoutDetails(workout) {
  workoutModal.value = {
    open: true,
    workout: workout
  }
}

function closeWorkoutModal() {
  workoutModal.value = {
    open: false,
    workout: null
  }
}

function formatCategory(category) {
  if (!category) return 'N/A'
  return category.replace(/_/g, ' ')
}

function getDifficultyClass(difficulty) {
  switch (difficulty) {
    case 'easy':
      return 'bg-emerald-100 text-emerald-800'
    case 'medium':
      return 'bg-amber-100 text-amber-800'
    case 'hard':
      return 'bg-rose-100 text-rose-800'
    default:
      return 'bg-slate-100 text-slate-800'
  }
}

onMounted(() => {
  // Fetch data from API
  fetchRecipes()
  fetchWorkouts()
  console.log('AdminDashboard mounted with all features: Dashboard, Users, Recipes, Workouts, and Coaches.')
})
</script>
